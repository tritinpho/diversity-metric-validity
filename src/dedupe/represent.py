"""Alternative pair representations for near-duplicate detection (Phase 2).

Round-1 calibration showed the production representation - multilingual MiniLM
over ``headline + body[:600]`` - is precision-safe but recall-poor: at the
configured 0.94 threshold, weighted recall inside the >=0.70 candidate pool is
~0.06, and weighted F1 peaks around 0.835 rather than at the operating point.

The diagnosis recorded in ``config.yaml`` is that the **representation**, not
the threshold, is the binding constraint. MiniLM truncates at 128 word-pieces
and Vietnamese sub-word-splits heavily, so a 600-character body consumes the
whole budget and the headline barely contributes - which is why
``embed_body_chars`` is measurably inert above ~600, and why two pairs with
byte-identical headlines scored only 0.78 and 0.81. Vietnamese syndication is
largely near-verbatim wire copy, a signal a *lexical* representation captures
directly and a truncated dense encoder throws away.

Human labels judge the **pair**, not any representation, so the existing labels
can be re-scored under any candidate at zero additional labelling cost. This
module defines the candidates and computes per-pair similarities;
``calibrate.py compare`` does the weighted scoring.

**What this comparison can and cannot establish.** The labelled pairs were drawn
from the pool the *baseline* representation puts at cosine >=0.70 (round 1) and
>=0.55 (round 2), so every estimate describes re-ranking **within that pool**. A
representation that would surface true same-story pairs the baseline scores
below the floor gets no credit for them, so a win here is evidence of better
ranking, not of identified absolute recall. Settling that needs a round drawn
under the winning representation's own bands - see ``calibrate.py``.

Pair similarities here are computed only for the articles that appear in
labelled pairs (a few hundred rows), so no run touches the production embedding
cache. The one piece that does scale is ``tfidf_matrix``, which
``calibrate.py`` reuses to score the whole analysis window when drawing a round
stratified on a lexical representation's own bands.
"""
from __future__ import annotations

import logging
import re
from typing import Any, Callable

import numpy as np

_LOG = logging.getLogger("vnnews.represent")

# Candidate representations. ``body_chars`` <= 0 means headline only.
#
# The set is chosen to separate three competing explanations for the round-1
# result: (a) the encoder's truncation budget is spent on body text
# (headline-only vs. body-bearing embeddings), (b) dense semantic similarity is
# the wrong family for near-verbatim republication (lexical vs. embedding), and
# (c) the signal is there but diluted by length (short vs. long body windows).
SPECS: dict[str, dict[str, Any]] = {
    # --- dense: the production baseline and its truncation-budget variants ---
    "emb_hl_body600": {
        "kind": "embedding", "body_chars": 600, "baseline": True,
        "note": "production representation (config: embed_body_chars=600)",
    },
    "emb_hl_body200": {
        "kind": "embedding", "body_chars": 200,
        "note": "short lead - leaves token budget for the headline",
    },
    "emb_hl_only": {
        "kind": "embedding", "body_chars": 0,
        "note": "headline only - no body dilution",
    },
    # --- lexical: near-verbatim republication is a surface-form signal ---
    "tfidf_char35_hl_body1200": {
        "kind": "tfidf", "body_chars": 1200, "analyzer": "char_wb",
        "ngram_range": (3, 5), "min_df": 3, "max_features": 400_000,
        "note": "char 3-5 grams - diacritic- and segmentation-agnostic",
    },
    "tfidf_char35_hl_only": {
        "kind": "tfidf", "body_chars": 0, "analyzer": "char_wb",
        "ngram_range": (3, 5), "min_df": 2, "max_features": 200_000,
        "note": "char 3-5 grams on the headline alone",
    },
    "tfidf_syl12_hl_body1200": {
        "kind": "tfidf", "body_chars": 1200, "analyzer": "word",
        "ngram_range": (1, 2), "min_df": 3, "max_features": 400_000,
        # Syllable unigrams+bigrams stand in for word segmentation: Vietnamese
        # compounds span syllables, and a bigram recovers most of them without
        # making the comparison depend on a segmenter version.
        "note": "syllable 1-2 grams - segmenter-free proxy for word tokens",
    },
    # --- set overlap: the classic near-duplicate signal, length-insensitive ---
    "jaccard_syl8_body3000": {
        "kind": "jaccard", "body_chars": 3000, "shingle": 8,
        "note": "Jaccard over 8-syllable shingles - verbatim-copy detector",
    },
    "jaccard_syl5_body3000": {
        "kind": "jaccard", "body_chars": 3000, "shingle": 5,
        "note": "shorter shingles - tolerates light rewriting",
    },
}

BASELINE = next(s for s, v in SPECS.items() if v.get("baseline"))


# ------------------------------------------------------------------- text prep
def build_texts(headlines, bodies, body_chars: int) -> list[str]:
    """Headline + leading body window, matching ``near_dup.assign_near_duplicates``.

    Kept byte-identical to the production construction so that the baseline
    similarities recomputed here reproduce the ones stored in the sample sheet —
    that agreement is what validates the pair-to-row mapping.
    """
    if body_chars <= 0:
        return [(h or "").strip() for h in headlines]
    return [((h or "") + ". " + (b or "")[:body_chars]).strip()
            for h, b in zip(headlines, bodies)]


_WS = re.compile(r"\s+")


def _syllables(text: str) -> list[str]:
    """Lowercased whitespace tokens. Vietnamese syllables, not words."""
    return _WS.split(text.strip().lower()) if text.strip() else []


# ---------------------------------------------------------------- similarities
def _sim_embedding(spec, texts, pairs, model_name) -> np.ndarray:
    from src.dedupe.near_dup import embed_texts

    emb = embed_texts(texts, model_name)          # already L2-normalized
    return np.einsum("ij,ij->i", emb[pairs[:, 0]], emb[pairs[:, 1]]).astype("float64")


def tfidf_matrix(spec: dict[str, Any], texts, fit_texts, dtype: str = "float64"):
    """L2-normalized TF-IDF matrix for ``texts``, with IDF fitted on ``fit_texts``.

    Shared by the pair-scoring path (a few hundred documents) and the
    corpus-scale scan in ``calibrate.py``, so a similarity computed either way is
    the same number by construction rather than by coincidence — the corpus scan
    checks exactly that against the stored per-pair scores before it is used.

    IDF is fitted on corpus text, not on the documents being scored: document
    frequencies estimated from ~400 labelled documents would be dominated by the
    sample itself and would not transfer to a full-corpus run. ``fit_texts``
    must therefore be built the same way at both scales — same sample, same
    seed, same row order — or the two disagree in the third decimal.
    """
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.preprocessing import normalize

    vec = TfidfVectorizer(
        analyzer=spec["analyzer"], ngram_range=tuple(spec["ngram_range"]),
        min_df=spec["min_df"], max_features=spec["max_features"],
        sublinear_tf=True, lowercase=True,
    )
    vec.fit(fit_texts)
    _LOG.info("  tfidf vocabulary: %d features", len(vec.vocabulary_))
    return normalize(vec.transform(texts)).astype(dtype)


def _sim_tfidf(spec, texts, pairs, fit_texts) -> np.ndarray:
    X = tfidf_matrix(spec, texts, fit_texts)
    return np.asarray(X[pairs[:, 0]].multiply(X[pairs[:, 1]]).sum(axis=1)).ravel()


def _sim_jaccard(spec, texts, pairs, _unused=None) -> np.ndarray:
    k = int(spec["shingle"])
    sets: list[set[int]] = []
    for t in texts:
        syl = _syllables(t)
        # Hash the shingles: the sets are only ever intersected, so the strings
        # themselves are never needed and hashing keeps memory flat.
        sets.append({hash(tuple(syl[i:i + k])) for i in range(len(syl) - k + 1)}
                    if len(syl) >= k else set())
    out = np.zeros(len(pairs), dtype="float64")
    for n, (a, b) in enumerate(pairs):
        sa, sb = sets[a], sets[b]
        union = len(sa | sb)
        out[n] = (len(sa & sb) / union) if union else 0.0
    return out


_DISPATCH: dict[str, Callable] = {
    "embedding": _sim_embedding,
    "tfidf": _sim_tfidf,
    "jaccard": _sim_jaccard,
}


def pair_similarities(
    slug: str, headlines, bodies, pairs: np.ndarray,
    model_name: str, fit_headlines=None, fit_bodies=None,
) -> np.ndarray:
    """Per-pair similarity under representation ``slug``.

    ``pairs`` is an (n, 2) array of row indices into ``headlines``/``bodies``.
    ``fit_*`` supply the corpus text used to fit IDF (tfidf specs only).
    """
    spec = SPECS[slug]
    # Only the rows a labelled pair actually points at are represented. Scoring
    # a few hundred pairs does not require encoding the whole analysis window,
    # and every representation here is per-document, so restricting the rows
    # leaves the similarities bit-identical. (Fitting IDF is separate and does
    # use corpus text -- see ``fit_*`` below.)
    uniq, inv = np.unique(pairs, return_inverse=True)
    pairs = inv.reshape(pairs.shape)
    headlines, bodies = np.asarray(headlines)[uniq], np.asarray(bodies)[uniq]
    texts = build_texts(headlines, bodies, spec["body_chars"])
    _LOG.info("representation %s (%s); %d documents for %d pairs",
              slug, spec["note"], len(uniq), len(pairs))

    if spec["kind"] == "tfidf":
        if fit_headlines is None:
            raise ValueError(f"{slug} needs corpus text to fit IDF")
        fit_texts = build_texts(fit_headlines, fit_bodies, spec["body_chars"])
        return _sim_tfidf(spec, texts, pairs, fit_texts)
    if spec["kind"] == "embedding":
        return _sim_embedding(spec, texts, pairs, model_name)
    return _sim_jaccard(spec, texts, pairs)
