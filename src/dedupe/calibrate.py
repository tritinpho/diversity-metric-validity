"""Threshold calibration for near-duplicate detection (Phase 2 validity work).

``dedupe.near_dup_threshold`` is currently justified by a comment in
``config.yaml``. That is not defensible in a measurement-validity paper: the
threshold sets how much cross-outlet overlap the corpus appears to contain, so
it needs an empirical precision/recall curve behind it, not an assertion.

This module builds that evidence in two steps::

    python -m src.dedupe.calibrate sample        # draw pairs, write labelling sheet
    # ...a human labels reports/calibration/pairs_sample.csv...
    python -m src.dedupe.calibrate score         # precision / recall by threshold

**Why stratified.** Within the analysis window there are ~40.7M candidate pairs
inside the 12h linkage window, of which only ~105k reach cosine 0.70 and ~2k
reach 0.94. True same-story pairs are far rarer still, so a uniform random
sample would return essentially no positives and support no recall estimate.
Instead pairs are binned by similarity, sampled within band, and each band is
re-weighted by its known population size when the rates are computed. Bands are
narrow around the decision boundary, where the threshold actually gets decided,
and coarse in the tail.

**What recall means here.** Recall is measured against the >=0.70 candidate pool,
not against all pairs. A same-story pair rewritten so heavily that it falls
below 0.70 is invisible to this design; the tail bands are sampled partly to
show whether that population looks non-empty. Report the figure as
"recall within the >=0.70 candidate pool" and not as unqualified recall.

The labelling sheet deliberately **hides the similarity score** — showing it
would anchor the labeller on the model's own answer — and interleaves bands in a
fixed-seed shuffle so labelling drift is not confounded with similarity.

**Bands belong to a representation.** Rounds 1-2 were stratified on MiniLM
cosine; round 3 is stratified on syllable TF-IDF, the representation the
comparison in ``represent.py`` showed to rank far better. A band edge is a
number on one of those scales and is meaningless on the other, so every strata
and sample file records the design it was drawn under and the pooling functions
refuse to mix them. Pass ``--design <slug>`` to ``score`` / ``compare`` to
choose. Rounds drawn on a *lexical* design need the corpus-scale similarity that
:func:`sparse_pair_scan` computes; the dense path keeps using the cached
embeddings.
"""
from __future__ import annotations

import argparse
import csv
import json
import logging
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from src.config import load_config, resolve_path, setup_logging
from src.dedupe.near_dup import embed_with_cache

_LOG = logging.getLogger("vnnews.calibrate")

# Round 1 (low, high, n_to_sample). Dense near the boundary, sparse in the tail.
BANDS_R1: list[tuple[float, float, int]] = [
    (0.70, 0.75, 8),
    (0.75, 0.80, 8),
    (0.80, 0.85, 12),
    (0.85, 0.88, 20),
    (0.88, 0.90, 25),
    (0.90, 0.92, 25),
    (0.92, 0.94, 30),   # just below threshold — decides whether 0.94 is too strict
    (0.94, 0.96, 30),
    (0.96, 0.98, 25),
    (0.98, 1.01, 25),
]

# Round 2 corrects two design errors that the round-1 labels exposed.
#
# (1) The 0.70 floor was too high. Confirmed same-story pairs turned up at
#     0.7157 and 0.7490 — right at the edge — so real positives certainly sit
#     below the old pool and were invisible to the estimate entirely.
# (2) The low bands were drastically under-sampled: [0.70,0.85) holds 85% of
#     the old pool but received 28 of 208 labels (0.03%, against 3.95% in the
#     top three bands). Recall at 0.94 came out 0.060 with a plausible range of
#     0.024-0.144 — i.e. not identified.
#
# Allocation leans toward the decision-relevant region (0.65-0.85) while still
# probing the three new bands hard enough to tell whether their rate is
# negligible or material. The high bands are untouched: precision up there is
# already well estimated and more labels would buy little.
BANDS_R2: list[tuple[float, float, int]] = [
    (0.55, 0.60, 15),
    (0.60, 0.65, 15),
    (0.65, 0.70, 18),
    (0.70, 0.75, 18),
    (0.75, 0.80, 14),
    (0.80, 0.85, 12),
]

# Round 3 abandons the dense representation's bands entirely. Rounds 1-2 were
# stratified on MiniLM cosine, which the representation comparison then showed
# to be the worst of eight candidates (weighted AP 0.581 vs 0.864 for syllable
# TF-IDF, paired bootstrap gain +0.257 [+0.064, +0.396]). Re-scoring the round-1
# labels under the winner answers "which representation ranks better", but not
# "where does its threshold go": the labelled pairs are still whatever the dense
# encoder happened to rank highly, so the syllable-TF-IDF bands they populate
# are an accident of the retired design. Round 3 is drawn under the adopted
# representation's own similarity, at corpus scale.
#
# Scale note: these are TF-IDF cosines and are NOT comparable to the 0.55-1.01
# numbers above. The pool floor is 0.10, chosen from the round-1 evidence that
# none of the 150 confirmed same-story pairs scored below 0.1344 under this
# representation — in a sample deliberately enriched for true pairs. Below the
# floor sit 3.06M pairs in [0.05, 0.10) and 19.4M in [0.025, 0.05); no feasible
# number of labels bounds a rate over populations that size, so that tail is
# declared out of scope rather than probed with a sample too small to speak.
# Recall from this round is therefore "within the >=0.10 syllable-TF-IDF pool".
#
# Allocation is Neyman (n_h proportional to N_h * sqrt(p_h(1-p_h))) under a
# prior p_h taken from the round-1 labels re-scored under this representation
# and deflated for their enrichment, with a floor of 8 per band so no band is
# unscoreable. That is what pushes a third of the budget into [0.10, 0.15):
# those bands hold 62% of the pool, and pool-level variance lives where the
# population is, not where the positives are. Round 1 allocated by intuition
# instead and put 28 of 208 labels into the bands holding 85% of its pool —
# the recorded defect this schedule exists to correct.
BANDS_R3: list[tuple[float, float, int]] = [
    (0.100, 0.125, 37),
    (0.125, 0.150, 24),
    (0.150, 0.175, 17),
    (0.175, 0.200, 14),
    (0.200, 0.225, 12),
    (0.225, 0.250, 10),
    (0.250, 0.300, 15),
    (0.300, 0.350, 10),
    (0.350, 0.400,  8),
    (0.400, 0.500,  8),
    (0.500, 0.650,  8),
    (0.650, 0.800,  8),
    (0.800, 1.010,  8),
]

ROUNDS = {1: BANDS_R1, 2: BANDS_R2, 3: BANDS_R3}

# The representation whose similarity each round was stratified on. This is the
# sampling *design*, so it is what weights, populations and band edges belong
# to: pooling rounds drawn under different designs would multiply a band's
# population by a label count from a different scale. Recorded in every strata
# and sample file from now on; files predating the field are round 1-2 and are
# read as the dense baseline.
ROUND_DESIGN = {1: "emb_hl_body600", 2: "emb_hl_body600",
                3: "tfidf_syl12_hl_body1200"}
LEGACY_DESIGN = ROUND_DESIGN[1]

FLOOR = 0.70          # round-1 floor, retained for the recall caveat wording
SEED = 20260722
PREVIEW_CHARS = 420
SCAN_BINS = 200       # similarity-histogram resolution for the sparse scan
RESERVOIR = 200       # pairs held per band during the scan, subsampled after


# ------------------------------------------------------------------ candidates
def _analysis_subset(df: pd.DataFrame, cfg: dict[str, Any]) -> pd.DataFrame:
    """Body-bearing rows inside the configured analysis window."""
    tz = cfg["project"]["timezone"]
    a = cfg.get("analysis") or {}
    out = df[df["body"].notna()]
    if a.get("start") and a.get("end"):
        dts = (pd.to_datetime(out["publish_datetime"], format="ISO8601",
                              errors="coerce", utc=True).dt.tz_convert(tz))
        lo = pd.Timestamp(str(a["start"]), tz=tz)
        hi = pd.Timestamp(str(a["end"]), tz=tz) + pd.Timedelta(days=1)
        out = out[(dts >= lo) & (dts < hi)]
    return out.reset_index(drop=True)


def candidate_pairs(
    emb: np.ndarray, secs: np.ndarray, max_hours: float, floor: float = FLOOR,
    block: int = 2000,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """All (i, j, sim) with sim >= floor and |t_i - t_j| <= max_hours.

    Rows must already be sorted by ``secs`` ascending. Mirrors the blocking and
    windowing in ``near_dup.cluster_near_dups`` so the sampled pool is exactly
    the population the clusterer draws its links from.
    """
    n = len(emb)
    hi = np.searchsorted(secs, secs + int(max_hours * 3600), side="right")
    I: list[np.ndarray] = []
    J: list[np.ndarray] = []
    S: list[np.ndarray] = []
    total = 0
    for s in range(0, n - 1, block):
        e = min(s + block, n)
        hm = int(hi[e - 1])
        if hm <= s + 1:
            continue
        sim = emb[s:e] @ emb[s:hm].T
        cols = np.arange(s, hm)[None, :]
        rows = np.arange(s, e)[:, None]
        valid = (cols > rows) & (cols < hi[s:e][:, None])
        total += int(valid.sum())
        keep = valid & (sim >= floor)
        bi, bj = np.nonzero(keep)
        if len(bi):
            I.append(bi + s)
            J.append(bj + s)
            S.append(sim[bi, bj])
    _LOG.info("candidate pairs within %gh: %d total, %d at cosine>=%.2f",
              max_hours, total, sum(len(x) for x in I), floor)
    if not I:
        return np.array([], "int64"), np.array([], "int64"), np.array([], "float32")
    return np.concatenate(I), np.concatenate(J), np.concatenate(S)


def _splitmix64(x: np.ndarray) -> np.ndarray:
    """Deterministic uint64 hash — the sampling key for the streaming scan.

    Keying on the pair's identity rather than on a sequential RNG makes the draw
    a pure function of ``(seed, i, j)``: it does not depend on block size, on
    iteration order, or on how many pairs happened to precede it. Without that,
    re-running the scan with a different ``block`` would silently return a
    different sample and the round would not be reproducible from config alone.
    """
    m = np.uint64(0xFFFFFFFFFFFFFFFF)
    z = (x + np.uint64(0x9E3779B97F4A7C15)) & m
    z = ((z ^ (z >> np.uint64(30))) * np.uint64(0xBF58476D1CE4E5B9)) & m
    z = ((z ^ (z >> np.uint64(27))) * np.uint64(0x94D049BB133111EB)) & m
    return z ^ (z >> np.uint64(31))


def sparse_pair_scan(
    X, secs: np.ndarray, max_hours: float, bands: list[tuple[float, float, int]],
    exclude_keys: np.ndarray | None = None, seed: int = SEED,
    block: int = 2048, capacity: int = RESERVOIR,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Corpus-scale sparse-cosine sweep: exact histogram + a sample per band.

    Mirrors :func:`candidate_pairs` — same blocking, same 12h forward window,
    same ``j > i`` triangle — but over a sparse TF-IDF matrix instead of dense
    embeddings, and it never materialises the pair list. At 46k rows the
    in-window population is ~40.7M pairs; storing ``(i, j, sim)`` for even the
    1% above the floor is avoidable, and storing all of them is not affordable.

    Two things come out of one pass:

    * a histogram on a fixed ``SCAN_BINS`` grid, which gives every band's
      population **exactly** — these are the Horvitz-Thompson denominators, so
      an approximation here would bias every weighted estimate downstream;
    * a bottom-k sample of ``capacity`` pairs per band, selected by the smallest
      ``_splitmix64`` key. Bottom-k on a uniform hash is a uniform sample without
      replacement of the band, equivalent to reservoir sampling but independent
      of arrival order. Held generously so the final per-band allocation can be
      decided after the populations are known and subsampled from it.

    Memory is bounded by one block's dense product. The TF-IDF rows share
    high-frequency Vietnamese syllables, so the block product comes out
    effectively dense (measured: 1.00) — densifying it is honest about what it
    already is, and costs ``block * window`` floats rather than the ~2x of
    carrying sparse indices for a matrix with no zeros in it.

    ``exclude_keys`` holds ``i * n + j`` for pairs drawn in earlier rounds. They
    are kept out of the sample but counted in the histogram, matching
    :func:`draw` — the population describes the whole band, the sample the
    not-yet-drawn remainder.
    """
    n = X.shape[0]
    if len(secs) != n:
        raise ValueError(f"secs has {len(secs)} rows, X has {n}")
    floor = min(lo for lo, _, _ in bands)
    # Bands are assigned with one searchsorted over their lower edges, which
    # silently folds any gap into the band below it — the pair would be sampled
    # there but not counted there, quietly corrupting that band's weight. Bands
    # must therefore tile the range without gaps or overlaps.
    for (_, prev_hi, _), (lo, _, _) in zip(bands, bands[1:]):
        if abs(prev_hi - lo) > 1e-12:
            raise ValueError(f"bands are not contiguous: {prev_hi} then {lo}")
    edges = np.array([lo for lo, _, _ in bands] + [bands[-1][1]], dtype="float64")

    hi = np.searchsorted(secs, secs + int(max_hours * 3600), side="right")
    hist = np.zeros(SCAN_BINS + 1, dtype="int64")
    # Bottom-k state per band, grown then trimmed each block.
    keep: list[dict[str, np.ndarray]] = [
        {"key": np.zeros(0, "uint64"), "i": np.zeros(0, "int64"),
         "j": np.zeros(0, "int64"), "s": np.zeros(0, "float64")} for _ in bands]
    total = 0

    for s in range(0, n - 1, block):
        e = min(s + block, n)
        hm = int(hi[e - 1])
        if hm <= s + 1:
            continue
        P = (X[s:e] @ X[s:hm].T).toarray()
        cols = np.arange(s, hm)[None, :]
        rows = np.arange(s, e)[:, None]
        valid = (cols > rows) & (cols < hi[s:e][:, None])
        total += int(valid.sum())
        hist += np.bincount(
            np.clip((P[valid] * SCAN_BINS).astype("int32"), 0, SCAN_BINS),
            minlength=SCAN_BINS + 1)

        bi, bj = np.nonzero(valid & (P >= floor))
        if not len(bi):
            del P, valid
            continue
        gi, gj = bi + s, bj + s
        sim = P[bi, bj].astype("float64")
        del P, valid

        pk = gi.astype("uint64") * np.uint64(n) + gj.astype("uint64")
        if exclude_keys is not None and len(exclude_keys):
            drop = np.isin(pk, exclude_keys)
            if drop.any():
                gi, gj, sim, pk = gi[~drop], gj[~drop], sim[~drop], pk[~drop]
        key = _splitmix64(pk ^ np.uint64(seed))
        # ``edges`` is the band grid; -1 / len(bands) mark out-of-range hits,
        # which only occur above the last band's top edge.
        slot = np.searchsorted(edges, sim, side="right") - 1
        for b in range(len(bands)):
            m = slot == b
            if not m.any():
                continue
            st = keep[b]
            k = np.concatenate([st["key"], key[m]])
            if len(k) > capacity:
                sel = np.argpartition(k, capacity)[:capacity]
            else:
                sel = np.arange(len(k))
            keep[b] = {
                "key": k[sel],
                "i": np.concatenate([st["i"], gi[m]])[sel],
                "j": np.concatenate([st["j"], gj[m]])[sel],
                "s": np.concatenate([st["s"], sim[m]])[sel],
            }

    _LOG.info("sparse scan within %gh: %d pairs, %d at similarity>=%.3f",
              max_hours, total, int(hist[int(round(floor * SCAN_BINS)):].sum()), floor)
    I = np.concatenate([st["i"] for st in keep]) if keep else np.zeros(0, "int64")
    J = np.concatenate([st["j"] for st in keep]) if keep else np.zeros(0, "int64")
    S = np.concatenate([st["s"] for st in keep]) if keep else np.zeros(0, "float64")
    return hist, I, J, S


def band_populations(hist: np.ndarray,
                     bands: list[tuple[float, float, int]]) -> dict[tuple[float, float], int]:
    """Exact per-band pair counts read off the scan histogram.

    Band edges must land on the ``SCAN_BINS`` grid; anything else would split a
    bin and make the population an interpolation rather than a count.
    """
    out: dict[tuple[float, float], int] = {}
    for lo, hi, _ in bands:
        a, b = lo * SCAN_BINS, hi * SCAN_BINS
        for edge in (a, b):
            if abs(edge - round(edge)) > 1e-9:
                raise ValueError(
                    f"band edge {edge / SCAN_BINS:.4f} is not on the 1/{SCAN_BINS} "
                    f"histogram grid, so its population cannot be counted exactly")
        out[(lo, hi)] = int(hist[int(round(a)):min(int(round(b)), SCAN_BINS + 1)].sum())
    return out


# --------------------------------------------------------------------- sampling
def draw(sub: pd.DataFrame, I, J, S, bands: list[tuple[float, float, int]],
         seed: int = SEED, exclude: set[frozenset] | None = None,
         populations: dict[tuple[float, float], int] | None = None,
         design: str = LEGACY_DESIGN,
) -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    """Stratified sample plus the per-band population sizes used to re-weight it.

    ``exclude`` holds ``frozenset({url_a, url_b})`` for pairs already drawn in an
    earlier round. Those are removed from the candidate pool *before* sampling
    but still counted in the band population, so the later round samples the
    remainder while the weights continue to describe the whole band. With
    sampling fractions well under 1% the two rounds can then be pooled and
    treated as one simple random sample per band.

    ``populations`` overrides the counts taken from ``S``. The dense path passes
    the whole candidate pool, so counting it directly is right; the sparse path
    passes only a per-band sample and carries the exact populations separately
    (see :func:`sparse_pair_scan`), where counting ``S`` would report the
    reservoir size as the band size and inflate every weight downstream.

    ``design`` names the representation whose similarity the bands are cut on
    and is stamped into both outputs, because a band edge means nothing without
    it — see :data:`ROUND_DESIGN`.
    """
    rng = np.random.default_rng(seed)
    exclude = exclude or set()
    urls = sub["url"].to_numpy()
    rows, strata = [], []
    for lo, hi, k in bands:
        idx = np.flatnonzero((S >= lo) & (S < hi))
        population = int(len(idx)) if populations is None else int(populations[(lo, hi)])
        if exclude:
            idx = np.array([p for p in idx
                            if frozenset((urls[I[p]], urls[J[p]])) not in exclude],
                           dtype="int64")
        take = min(k, len(idx))
        if take < k:
            _LOG.warning("band [%.3f,%.3f): wanted %d pairs, only %d available",
                         lo, hi, k, take)
        pick = rng.choice(idx, size=take, replace=False) if take else np.array([], "int64")
        strata.append({"band_lo": lo, "band_hi": hi, "representation": design,
                       "population": population, "sampled": int(take)})
        for p in pick:
            a, b = int(I[p]), int(J[p])
            ra, rb = sub.iloc[a], sub.iloc[b]
            rows.append({
                "pair_id": f"{ra.article_id[:8]}_{rb.article_id[:8]}",
                "representation": design,
                "band_lo": lo, "band_hi": hi, "similarity": round(float(S[p]), 4),
                "cross_outlet": int(ra.outlet != rb.outlet),
                "outlet_a": ra.outlet, "published_a": str(ra.publish_datetime),
                "headline_a": ra.headline, "lead_a": (ra.body or "")[:PREVIEW_CHARS],
                "url_a": ra.url,
                "outlet_b": rb.outlet, "published_b": str(rb.publish_datetime),
                "headline_b": rb.headline, "lead_b": (rb.body or "")[:PREVIEW_CHARS],
                "url_b": rb.url,
                "label": "", "notes": "",
            })
    out = pd.DataFrame(rows)
    # Interleave bands so labelling fatigue is not confounded with similarity.
    out = out.sample(frac=1.0, random_state=SEED).reset_index(drop=True)
    return out, strata


_HTML = """<!doctype html><meta charset="utf-8"><title>Near-dup labelling</title>
<style>
 body{font:15px/1.55 system-ui,sans-serif;max-width:1180px;margin:0 auto;padding:24px;background:#faf9f7;color:#1a1a1a}
 h1{font-size:19px;margin:0 0 4px} .sub{color:#666;font-size:13px;margin-bottom:18px}
 #bar{position:sticky;top:0;background:#faf9f7;padding:12px 0;border-bottom:1px solid #ddd;z-index:9}
 .pair{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin:18px 0}
 .side{background:#fff;border:1px solid #e2e0dc;border-radius:8px;padding:14px}
 .meta{font-size:12px;color:#777;margin-bottom:6px}
 .hl{font-weight:600;margin-bottom:8px} .lead{font-size:14px;color:#333}
 .btns{display:flex;gap:8px;margin:10px 0 4px}
 button{font:inherit;padding:8px 18px;border-radius:6px;border:1px solid #ccc;background:#fff;cursor:pointer}
 button:hover{background:#f0efec}
 .y{border-color:#2d7a3e;color:#2d7a3e} .n{border-color:#a33;color:#a33}
 .done{opacity:.45} .cur{outline:2px solid #3b76a8;outline-offset:6px;border-radius:10px}
 #dl{background:#1a1a1a;color:#fff;border-color:#1a1a1a}
 kbd{background:#eee;border:1px solid #ccc;border-radius:3px;padding:1px 5px;font-size:12px}
</style>
<h1>Near-duplicate labelling</h1>
<div class="sub">Same <b>story</b> = the two articles report the same specific event/announcement.
Not the same story = same topic, recurring column, or a later development with new facts.
Similarity scores are hidden on purpose. <kbd>y</kbd> same &middot; <kbd>n</kbd> different &middot; <kbd>s</kbd> skip &middot; <kbd>u</kbd> undo</div>
<div id="bar"><span id="prog"></span> &nbsp; <button id="dl">Download labels CSV</button>
 <span id="saved" style="color:#2d7a3e;font-size:12px"></span></div>
<div id="list"></div>
<script>
// KEY is per-sheet, not per-round: the reliability sheet re-labels pairs the
// primary sheet also holds, and a shared key would hand the second coder the
// first coder's answers out of localStorage.
const D=__DATA__, KEY='near-dup-labels-__STEM__'; let cur=0;
const L=document.getElementById('list'), P=document.getElementById('prog');
// Labels live only in this page until downloaded, so mirror them to
// localStorage on every keystroke — a refresh or accidental close would
// otherwise discard the whole session's work.
try{const s=JSON.parse(localStorage.getItem(KEY)||'{}');
    D.forEach(d=>{if(s[d.pair_id]!==undefined)d.label=s[d.pair_id]})}catch(e){}
function save(){try{const s={};D.forEach(d=>{if(d.label!==undefined)s[d.pair_id]=d.label});
 localStorage.setItem(KEY,JSON.stringify(s));
 document.getElementById('saved').textContent='saved locally'}catch(e){}}
D.forEach((d,i)=>{
 const el=document.createElement('div'); el.id='p'+i;
 el.innerHTML=`<div class="btns"><b>${i+1}.</b>
   <button class="y" onclick="mark(${i},1)">Same story</button>
   <button class="n" onclick="mark(${i},0)">Different</button>
   <button onclick="mark(${i},'')">Skip</button>
   <span id="s${i}" style="color:#666"></span></div>
  <div class="pair">
   <div class="side"><div class="meta">${d.outlet_a} &middot; ${d.published_a}
     &middot; <a href="${esc(d.url_a)}" target="_blank" rel="noopener">open source ↗</a></div>
     <div class="hl">${esc(d.headline_a)}</div><div class="lead">${esc(d.lead_a)}…</div></div>
   <div class="side"><div class="meta">${d.outlet_b} &middot; ${d.published_b}
     &middot; <a href="${esc(d.url_b)}" target="_blank" rel="noopener">open source ↗</a></div>
     <div class="hl">${esc(d.headline_b)}</div><div class="lead">${esc(d.lead_b)}…</div></div>
  </div>`;
 L.appendChild(el);
 if(d.label!==undefined)paint(i);
});
function esc(s){const d=document.createElement('div');d.textContent=s||'';return d.innerHTML}
function paint(i){const v=D[i].label;
 document.getElementById('s'+i).textContent=v===1?'✓ same':(v===0?'✗ different':'skipped');
 document.getElementById('p'+i).classList.add('done')}
function mark(i,v){D[i].label=v;paint(i);save();
 if(i===cur)focus(Math.min(cur+1,D.length-1));upd()}
function focus(i){document.getElementById('p'+cur)?.classList.remove('cur');cur=i;
 const el=document.getElementById('p'+i);el.classList.add('cur');el.scrollIntoView({block:'center',behavior:'smooth'});upd()}
function upd(){const n=D.filter(d=>d.label!==''&&d.label!==undefined).length;P.textContent=`${n} / ${D.length} labelled — on #${cur+1}`}
addEventListener('keydown',e=>{if(e.target.tagName==='A')return;
 if(e.key==='y')mark(cur,1);else if(e.key==='n')mark(cur,0);
 else if(e.key==='s')mark(cur,'');else if(e.key==='u')focus(Math.max(0,cur-1));});
addEventListener('beforeunload',e=>{const n=D.filter(d=>d.label!==''&&d.label!==undefined).length;
 if(n>0&&!window.__dl){e.preventDefault();e.returnValue=''}});
document.getElementById('dl').onclick=()=>{window.__dl=1;
 const cols=['pair_id','representation','similarity','band_lo','band_hi','cross_outlet','label'];
 const rows=[cols.join(',')].concat(D.map(d=>cols.map(c=>{
   const v=d[c]===undefined?'':d[c];return /[",\\n]/.test(''+v)?'"'+(''+v).replace(/"/g,'""')+'"':v}).join(',')));
 const b=new Blob([rows.join('\\n')],{type:'text/csv;charset=utf-8'});
 const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='__STEM__.csv';a.click()};
focus(0);upd();
</script>
"""


def write_sheets(sample: pd.DataFrame, strata: list[dict], outdir: Path,
                 suffix: str = "", csv_name: str | None = None,
                 html_name: str | None = None,
                 strata_name: str | None = "strata{suffix}.json",
) -> tuple[Path, Path, Path | None]:
    """Write the labelling sheet as CSV + standalone HTML, plus its strata.

    The names are overridable so the second-coder sheet can live outside the
    ``pairs_*`` family that :func:`score` and :func:`compare` glob — see
    :data:`RELIABILITY_SHEET`. ``strata_name=None`` skips the strata file, which
    a reliability subset has no business writing: it is a re-labelling of pairs
    already drawn, not a new sample with its own inclusion probabilities.
    """
    outdir.mkdir(parents=True, exist_ok=True)
    csv_p = outdir / (csv_name or f"pairs_sample{suffix}.csv")
    sample.to_csv(csv_p, index=False, encoding="utf-8-sig", quoting=csv.QUOTE_MINIMAL)

    keep = ["pair_id", "representation", "similarity", "band_lo", "band_hi",
            "cross_outlet",
            "outlet_a", "published_a", "headline_a", "lead_a", "url_a",
            "outlet_b", "published_b", "headline_b", "lead_b", "url_b"]
    # No initial ``label`` key: undefined means untouched, "" means deliberately
    # skipped, 0/1 means judged. Seeding it with "" would make every pair look
    # pre-skipped on load and defeat the restore-from-storage check.
    payload = sample[keep].to_dict("records")
    html_p = outdir / (html_name or f"label{suffix}.html")
    # The stem names both the downloaded CSV and the localStorage key, so two
    # sheets covering the same pairs stay independent of each other.
    stem = (f"reliability_labelled{suffix}" if html_name
            else f"pairs_labelled{suffix}")
    html_p.write_text(_HTML.replace("__DATA__", json.dumps(payload, ensure_ascii=False))
                           .replace("__STEM__", stem),
                      encoding="utf-8")

    if strata_name is None:
        return csv_p, html_p, None
    strata_p = outdir / strata_name.format(suffix=suffix)
    strata_p.write_text(json.dumps(strata, indent=2), encoding="utf-8")
    return csv_p, html_p, strata_p


# ---------------------------------------------------------------------- scoring
def score(labels: pd.DataFrame, strata: list[dict]) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Stratum-weighted precision / recall / F1 at each band edge.

    Each band's labelled positive rate is extrapolated to its full population,
    so the estimates describe the whole >=0.70 candidate pool rather than the
    sample. Thresholds are evaluated only at band edges — interpolating inside a
    band would assume a within-band distribution the sample cannot support.

    A band with no labels contributes zero estimated positives, which would
    quietly inflate precision and distort recall, so partial labelling raises
    rather than silently producing a plausible-looking curve.
    """
    lab = labels[labels["label"].isin([0, 1, "0", "1"])].copy()
    lab["label"] = lab["label"].astype(int)
    pop = {(s["band_lo"], s["band_hi"]): s["population"] for s in strata}

    est = []
    for (lo, hi), N in sorted(pop.items()):
        sl = lab[(lab["band_lo"] == lo) & (lab["band_hi"] == hi)]
        n, k = len(sl), int(sl["label"].sum())
        rate = (k / n) if n else float("nan")
        est.append({"lo": lo, "hi": hi, "N": N, "n": n, "k": k,
                    "rate": rate, "P": (N * rate) if n else 0.0})
    e = pd.DataFrame(est)

    empty = e[e["n"] == 0]
    if len(empty):
        raise SystemExit(
            "cannot score: no labels in band(s) "
            + ", ".join(f"[{r.lo:.2f},{r.hi:.2f})" for r in empty.itertuples())
            + ". An unlabelled band would be counted as containing zero true "
              "pairs, inflating precision and understating the true-pair total. "
              "Label at least a few pairs in every band, or drop those bands "
              "from strata.json deliberately.")
    thin = e[(e["n"] > 0) & (e["n"] < 5)]
    if len(thin):
        _LOG.warning("bands with <5 labels — rates there are very noisy: %s",
                     ", ".join(f"[{r.lo:.2f},{r.hi:.2f}) n={r.n}"
                               for r in thin.itertuples()))
    _LOG.info("scoring on %d labelled pairs of %d sampled", len(lab), len(labels))
    total_pos = e["P"].sum()

    rows = []
    for lo in sorted(e["lo"]):
        sel = e[e["lo"] >= lo]
        retrieved, tp = sel["N"].sum(), sel["P"].sum()
        prec = tp / retrieved if retrieved else float("nan")
        rec = tp / total_pos if total_pos else float("nan")
        f1 = (2 * prec * rec / (prec + rec)) if (prec + rec) else float("nan")
        rows.append({"threshold": lo, "pairs_retrieved": int(retrieved),
                     "est_true_pairs": round(tp, 1), "precision": round(prec, 3),
                     "recall_in_pool": round(rec, 3), "f1": round(f1, 3)})
    return pd.DataFrame(rows), e


def operating_point(tbl: pd.DataFrame, min_precision: float) -> pd.Series | None:
    """The pre-registered operating threshold: lowest one reaching the precision floor.

    Fixed in advance of seeing the labels (``config.yaml``:
    ``dedupe.near_dup_min_precision``) so the reported operating point is not
    selected on the same labels that score it — unlike the ``best_f1`` column
    elsewhere in this module, which is an upper bound for exactly that reason.

    Lowest rather than highest: among thresholds meeting the precision floor,
    the lowest keeps the most true pairs, so the rule buys recall subject to a
    precision constraint rather than trading both away.
    """
    ok = tbl[tbl["precision"] >= min_precision]
    return None if ok.empty else ok.loc[ok["threshold"].idxmin()]


# ------------------------------------------------------- representation compare
def _labelled_with_context(outdir: Path, design: str | None = None) -> pd.DataFrame:
    """Pool the labelled rounds drawn under one sampling design.

    The labelling sheet exports only ``pair_id`` and the judgment, so the pair's
    endpoints have to come back from the corresponding ``pairs_sample*.csv``.
    The sheet is also what says which representation the pair's band edges were
    cut on — authoritative over the label file, which may predate the field.

    Rounds drawn under different designs are **not** pooled. Their band edges
    are numbers on different similarity scales, so a shared ``[0.70, 0.75)`` key
    would pair one design's label count with another's population. ``design``
    selects one; with several present and none named, this raises rather than
    picking for you.
    """
    label_files = sorted(outdir.glob("pairs_labelled*.csv"))
    if not label_files:
        raise SystemExit(f"no labelled files in {outdir} — label a sheet first")
    labels = pd.concat([pd.read_csv(p) for p in label_files], ignore_index=True)
    labels = labels.drop_duplicates("pair_id")
    labels = labels[labels["label"].isin([0, 1, "0", "1"])].copy()
    labels["label"] = labels["label"].astype(int)

    sheets = pd.concat([pd.read_csv(p) for p in sorted(outdir.glob("pairs_sample*.csv"))],
                       ignore_index=True).drop_duplicates("pair_id")
    if "representation" not in sheets.columns:
        sheets["representation"] = LEGACY_DESIGN
    sheets["representation"] = sheets["representation"].fillna(LEGACY_DESIGN)
    cols = ["pair_id", "url_a", "url_b", "band_lo", "band_hi", "similarity",
            "cross_outlet", "representation"]
    out = labels[["pair_id", "label"]].merge(sheets[cols], on="pair_id", how="left")
    missing = out["url_a"].isna()
    if missing.any():
        raise SystemExit(
            f"{int(missing.sum())} labelled pair(s) have no matching row in any "
            f"pairs_sample*.csv — the sheets and labels are out of sync.")

    design = _pick_design(sorted(out["representation"].unique()), design, "labelled pairs")
    out = out[out["representation"] == design].reset_index(drop=True)
    _LOG.info("pooled %d labelled pairs stratified on %s (from %s)", len(out),
              design, ", ".join(p.name for p in label_files))
    return out


def _pick_design(present: list[str], requested: str | None, what: str) -> str:
    """Resolve which sampling design to work with, or fail with the options."""
    if requested is not None:
        if requested not in present:
            raise SystemExit(
                f"no {what} stratified on '{requested}'. Present: "
                f"{', '.join(present) or '(none)'}")
        return requested
    if not present:
        raise SystemExit(f"no {what} found")
    if len(present) > 1:
        raise SystemExit(
            f"{what} span {len(present)} sampling designs ({', '.join(present)}) "
            f"and cannot be pooled — their band edges are on different similarity "
            f"scales. Re-run with --design <representation>.")
    return present[0]


def _weights(lab: pd.DataFrame, strata: list[dict[str, Any]]) -> np.ndarray:
    """Horvitz-Thompson weight per labelled pair: band population / band labels.

    Sampling was stratified on the *baseline* representation's similarity, so
    every weighted estimate below describes the baseline's candidate pool. The
    weight attaches to the pair, not to the score, which is exactly why an
    alternative representation can be evaluated on the same labels: only the
    quantity being thresholded changes, not the sampling design.
    """
    pop = {(s["band_lo"], s["band_hi"]): s["population"] for s in strata}
    n_lab = lab.groupby(["band_lo", "band_hi"]).size()
    w = np.zeros(len(lab), dtype="float64")
    for (lo, hi), n in n_lab.items():
        if (lo, hi) not in pop:
            raise SystemExit(f"band [{lo},{hi}) has labels but no strata entry")
        w[((lab["band_lo"] == lo) & (lab["band_hi"] == hi)).to_numpy()] = pop[(lo, hi)] / n
    unlabelled = [k for k in pop if k not in set(n_lab.index)]
    if unlabelled:
        _LOG.warning(
            "%d sampled band(s) carry no labels and are excluded from the pool: %s "
            "- estimates describe only the labelled bands",
            len(unlabelled), ", ".join(f"[{lo:.2f},{hi:.2f})" for lo, hi in sorted(unlabelled)))
    return w


def _curve(sim: np.ndarray, y: np.ndarray, w: np.ndarray) -> pd.DataFrame:
    """Weighted precision / recall / F1 at every distinct score in the sample."""
    total_pos = float((w * y).sum())
    rows = []
    for t in np.unique(sim):
        sel = sim >= t
        retrieved = float(w[sel].sum())
        tp = float((w[sel] * y[sel]).sum())
        prec = tp / retrieved if retrieved else float("nan")
        rec = tp / total_pos if total_pos else float("nan")
        f1 = (2 * prec * rec / (prec + rec)) if (prec + rec) else 0.0
        rows.append({"threshold": float(t), "pairs_retrieved": retrieved,
                     "est_true_pairs": tp, "precision": prec,
                     "recall_in_pool": rec, "f1": f1})
    return pd.DataFrame(rows)


def bootstrap_compare(
    sims: dict[str, np.ndarray], y: np.ndarray, w: np.ndarray,
    bands: np.ndarray, draws: int = 2000, seed: int = SEED,
) -> tuple[pd.DataFrame, dict[str, float]]:
    """Stratified bootstrap over the labels, resampling within band.

    The point estimates hide how thin the evidence under them is: the low bands
    hold most of the candidate pool but carry a handful of labels each, so one
    weighted label moves a pool-level total by thousands of pairs. Resampling
    within band (which is how the sample was drawn) propagates that into every
    reported quantity.

    Which representation is better is a separate question from how good either
    one is, and it is answered far more sharply — see ``paired_gain``.
    """
    from sklearn.metrics import average_precision_score

    rng = np.random.default_rng(seed)
    groups = [np.flatnonzero(bands == b) for b in np.unique(bands)]
    ap: dict[str, list[float]] = {s: [] for s in sims}
    totals: list[float] = []

    for _ in range(draws):
        idx = np.concatenate([rng.choice(g, size=len(g), replace=True) for g in groups])
        yy, ww = y[idx], w[idx]
        totals.append(float((ww * yy).sum()))
        if yy.sum() == 0 or yy.sum() == len(yy):
            continue                      # AP undefined on a one-class resample
        for s, v in sims.items():
            ap[s].append(average_precision_score(yy, v[idx], sample_weight=ww))

    def ci(v):
        return (float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5)))

    rows = []
    for s in sims:
        lo, hi = ci(ap[s])
        rows.append({"representation": s, "ap_w_lo": lo, "ap_w_hi": hi})
    extra = {"est_true_lo": ci(totals)[0], "est_true_hi": ci(totals)[1],
             "est_true_mean": float(np.mean(totals)), "draws": draws}
    return pd.DataFrame(rows), extra


def paired_gain(
    sims: dict[str, np.ndarray], y: np.ndarray, w: np.ndarray, bands: np.ndarray,
    challenger: str, baseline: str, draws: int = 2000, seed: int = SEED,
) -> dict[str, float]:
    """Paired bootstrap of AP(w) for ``challenger`` minus ``baseline``."""
    from sklearn.metrics import average_precision_score

    rng = np.random.default_rng(seed)
    groups = [np.flatnonzero(bands == b) for b in np.unique(bands)]
    d = []
    for _ in range(draws):
        idx = np.concatenate([rng.choice(g, size=len(g), replace=True) for g in groups])
        yy, ww = y[idx], w[idx]
        if yy.sum() == 0 or yy.sum() == len(yy):
            continue
        d.append(average_precision_score(yy, sims[challenger][idx], sample_weight=ww)
                 - average_precision_score(yy, sims[baseline][idx], sample_weight=ww))
    d = np.asarray(d)
    return {"mean": float(d.mean()), "lo": float(np.percentile(d, 2.5)),
            "hi": float(np.percentile(d, 97.5)), "p_positive": float((d > 0).mean())}


def compare_representations(
    sub: pd.DataFrame, lab: pd.DataFrame, strata: list[dict[str, Any]],
    model_name: str, slugs: list[str], fit_n: int = 15000, seed: int = SEED,
) -> tuple[pd.DataFrame, dict[str, np.ndarray], pd.DataFrame]:
    """Rank candidate representations on the same labels, weights and pairs.

    Returns the per-representation summary, the raw per-pair similarities, and
    the labelled frame they align to — so the winner's full curve and its
    disagreements with the baseline can be inspected, not just its best point.
    """
    from sklearn.metrics import average_precision_score, roc_auc_score

    from src.dedupe import represent

    pos = {u: i for i, u in enumerate(sub["url"].to_numpy())}
    idx_a = lab["url_a"].map(pos)
    idx_b = lab["url_b"].map(pos)
    if idx_a.isna().any() or idx_b.isna().any():
        raise SystemExit(
            f"{int(idx_a.isna().sum() + idx_b.isna().sum())} labelled endpoint(s) "
            f"are not in the analysis subset — the corpus or the analysis window "
            f"changed since the sample was drawn, so the labels cannot be reused.")
    pairs = np.column_stack([idx_a.to_numpy(dtype="int64"),
                             idx_b.to_numpy(dtype="int64")])

    y = lab["label"].to_numpy()
    w = _weights(lab, strata)
    keep = w > 0                      # drop bands excluded for having no labels
    pairs, y, w = pairs[keep], y[keep], w[keep]
    lab = lab[keep].reset_index(drop=True)
    _LOG.info("comparing on %d labelled pairs (%d positive), representing "
              "%.0f pairs in the candidate pool", len(y), int(y.sum()), w.sum())

    # IDF is fitted on a fixed-seed corpus sample rather than the full subset:
    # char 3-5 grams over 46k full bodies is minutes of work per representation
    # and document frequencies are already stable at this size.
    fit = sub.sample(n=min(fit_n, len(sub)), random_state=seed)

    rows, sims = [], {}
    for slug in slugs:
        s = represent.pair_similarities(
            slug, sub["headline"].to_numpy(), sub["body"].to_numpy(), pairs,
            model_name, fit["headline"].to_numpy(), fit["body"].to_numpy())
        sims[slug] = s
        curve = _curve(s, y, w)
        best = curve.loc[curve["f1"].idxmax()]
        rows.append({
            "representation": slug,
            "auc_w": roc_auc_score(y, s, sample_weight=w),
            "ap_w": average_precision_score(y, s, sample_weight=w),
            "auc_raw": roc_auc_score(y, s),
            "best_f1": best["f1"], "at_threshold": best["threshold"],
            "precision": best["precision"], "recall_in_pool": best["recall_in_pool"],
            "est_true_pairs": best["est_true_pairs"],
            "pairs_retrieved": best["pairs_retrieved"],
        })
        _LOG.info("  %-26s AUC(w)=%.3f  AP(w)=%.3f  best F1=%.3f @ %.3f",
                  slug, rows[-1]["auc_w"], rows[-1]["ap_w"],
                  best["f1"], best["threshold"])

    out = pd.DataFrame(rows).sort_values("ap_w", ascending=False).reset_index(drop=True)
    lab = lab.assign(weight=w)
    return out, sims, lab


# --------------------------------------------------------------- inter-rater
# The reliability sheet is deliberately named outside the ``pairs_*`` family.
# ``score`` and ``compare`` glob ``pairs_labelled*.csv`` and pool what they find,
# so a second coder's file under that name would be silently merged into the
# primary labels and de-duplicated to whichever row landed first.
RELIABILITY_SHEET = "reliability_sample{suffix}.csv"
RELIABILITY_HTML = "reliability{suffix}.html"


def reliability_subset(sample: pd.DataFrame, n: int, seed: int = SEED) -> pd.DataFrame:
    """A simple random subsample of a round, for a second coder to label blind.

    Simple random rather than stratified: the estimand is agreement over *this
    round's* labels, so the overlap should mirror the round's own composition.
    Re-stratifying it toward the ambiguous middle would measure reliability on a
    harder population than the one the labels actually come from.

    Re-ordered under a different seed so the two coders meet the pairs in
    different sequences and any fatigue or drift does not correlate between them.
    """
    if n > len(sample):
        raise SystemExit(f"asked for {n} pairs, the round has {len(sample)}")
    sub = sample.sample(n=n, random_state=seed)
    return sub.sample(frac=1.0, random_state=seed + 1).reset_index(drop=True)


def agreement(a: pd.DataFrame, b: pd.DataFrame) -> dict[str, Any]:
    """Observed agreement, Cohen's kappa and Krippendorff's alpha on binary labels.

    The two chance corrections differ in more than sample size, and both are
    reported because they can disagree: kappa's expected agreement multiplies
    each coder's *own* marginal, alpha's uses the *pooled* marginal over all
    values. Alpha follows the coincidence-matrix definition, whose units are
    values (two per pair, so ``2n``), not pairs — putting the ``(N-1)/N``
    correction on ``n`` instead of ``2n`` is an easy and silent error.
    """
    m = a.merge(b, on="pair_id", suffixes=("_a", "_b"))
    m = m[m["label_a"].isin([0, 1]) & m["label_b"].isin([0, 1])]
    n = len(m)
    if n == 0:
        raise SystemExit("no pair is labelled by both coders")
    x, y = m["label_a"].to_numpy(int), m["label_b"].to_numpy(int)
    po = float((x == y).mean())

    # Cohen: expected agreement from each coder's own marginal.
    pe = sum(float((x == v).mean()) * float((y == v).mean()) for v in (0, 1))
    kappa = (po - pe) / (1 - pe) if pe < 1 else float("nan")

    # Krippendorff, from the coincidence matrix. With two coders and no missing
    # values each pair contributes two values, so N = 2n; the off-diagonal mass
    # is 2d for d disagreeing pairs.
    #   D_o = 2d / N
    #   D_e = 2*n_0*n_1 / (N*(N-1))
    d = int((x != y).sum())
    N = 2 * n
    n1 = int(x.sum() + y.sum())
    n0 = N - n1
    do = 2 * d / N
    de = 2 * n0 * n1 / (N * (N - 1)) if N > 1 else 0.0
    alpha = 1 - do / de if de > 0 else float("nan")

    return {"n": n, "observed_agreement": po, "cohen_kappa": kappa,
            "krippendorff_alpha": alpha,
            "positives_a": int(x.sum()), "positives_b": int(y.sum()),
            "disagreements": int((x != y).sum())}


# ------------------------------------------------------------------------- main
def _sparse_pool(
    sub: pd.DataFrame, fit: pd.DataFrame, secs: np.ndarray, max_hours: float,
    bands: list[tuple[float, float, int]], design: str,
    exclude: set[frozenset], scores_csv: Path, seed: int = SEED,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, dict[tuple[float, float], int]]:
    """Candidate pool for a lexical design: build the matrix, verify it, scan it.

    Returns the per-band sample and the exact band populations, in the shape
    :func:`draw` expects. The verification step in the middle is not optional:
    the whole point of stratifying on this representation is that its scores are
    the ones already measured against human labels, so if the corpus-scale
    matrix reproduces different numbers than ``compare`` stored, the bands are
    cut on a different quantity than the one they claim and the round is void.
    """
    from src.dedupe import represent

    spec = represent.SPECS[design]
    if spec["kind"] != "tfidf":
        raise SystemExit(f"design '{design}' is {spec['kind']}; the corpus-scale "
                         f"scan is only implemented for tfidf representations")
    bc = spec["body_chars"]
    X = represent.tfidf_matrix(
        spec,
        represent.build_texts(sub["headline"].to_numpy(), sub["body"].to_numpy(), bc),
        represent.build_texts(fit["headline"].to_numpy(), fit["body"].to_numpy(), bc),
        dtype="float32")
    _LOG.info("%s matrix: %d x %d, %d nonzeros (%.0f/row)",
              design, X.shape[0], X.shape[1], X.nnz, X.nnz / X.shape[0])

    pos = {u: i for i, u in enumerate(sub["url"].to_numpy())}
    _verify_against_stored(X, pos, design, scores_csv)

    # Excluded pairs are matched on row index, not URL: the scan sees tens of
    # millions of pairs and a per-pair Python set lookup would dominate its cost.
    n = len(sub)
    ek: set[int] = set()
    for f in exclude:
        rows = [pos[u] for u in f if u in pos]
        if len(rows) == 2:
            ek.add(min(rows) * n + max(rows))
    hist, I, J, S = sparse_pair_scan(
        X, secs, max_hours, bands,
        exclude_keys=np.array(sorted(ek), dtype="uint64"), seed=seed)
    populations = band_populations(hist, bands)
    for lo, hi, k in bands:
        held = int(((S >= lo) & (S < hi)).sum())
        if held < k:
            _LOG.warning("band [%.3f,%.3f) held only %d of the %d pairs wanted "
                         "(population %d) — raise RESERVOIR if this is not simply "
                         "a small band", lo, hi, held, k, populations[(lo, hi)])
    return I, J, S, populations


def _verify_against_stored(X, pos: dict[str, int], design: str,
                           scores_csv: Path, tol: float = 1e-4) -> None:
    """Check the corpus matrix reproduces the per-pair scores ``compare`` wrote."""
    if not scores_csv.exists():
        _LOG.warning("no %s on disk — corpus-scale %s scores are unverified "
                     "against the labelled-pair run", scores_csv.name, design)
        return
    sc = pd.read_csv(scores_csv)
    outdir = scores_csv.parent
    sheets = pd.concat([pd.read_csv(p) for p in sorted(outdir.glob("pairs_sample*.csv"))],
                       ignore_index=True).drop_duplicates("pair_id")
    if design not in sc.columns:
        _LOG.warning("%s has no '%s' column — skipping the reproduction check",
                     scores_csv.name, design)
        return
    m = sc[["pair_id", design]].merge(sheets[["pair_id", "url_a", "url_b"]],
                                      on="pair_id", how="inner")
    m = m[m["url_a"].map(pos).notna() & m["url_b"].map(pos).notna()]
    if m.empty:
        _LOG.warning("no stored %s scores could be matched — check skipped", design)
        return
    ia = m["url_a"].map(pos).to_numpy("int64")
    ib = m["url_b"].map(pos).to_numpy("int64")
    got = np.asarray(X[ia].multiply(X[ib]).sum(axis=1)).ravel()
    drift = float(np.abs(got - m[design].to_numpy()).max())
    _LOG.info("%s reproduction check on %d stored pairs: max |delta| = %.2e",
              design, len(m), drift)
    if drift > tol:
        raise SystemExit(
            f"the corpus-scale {design} matrix disagrees with the scores in "
            f"{scores_csv.name} by up to {drift:.4f}. The bands would be cut on a "
            f"different quantity than the one the representation comparison "
            f"measured. Most likely the IDF-fit sample differs (size, seed, or row "
            f"order) — it must match compare_representations exactly.")


def _merge_strata(outdir: Path, design: str | None = None) -> list[dict[str, Any]]:
    """Union the strata files drawn under one design: population fixed, samples add.

    Rounds stratified on different representations are kept apart for the reason
    in :func:`_labelled_with_context` — the band keys collide numerically while
    meaning different things.
    """
    loaded: list[dict[str, Any]] = []
    for p in sorted(outdir.glob("strata*.json")):
        for s in json.loads(p.read_text(encoding="utf-8")):
            # ``retired`` bands were drawn but deliberately abandoned unlabelled.
            # Keeping them would make score() refuse to run for want of labels
            # that are never coming; dropping them narrows the pool the estimates
            # describe, which is why it has to be recorded in the file rather
            # than inferred from the absence of labels.
            if s.get("retired"):
                _LOG.info("skipping retired band [%.2f,%.2f) from %s",
                          s["band_lo"], s["band_hi"], p.name)
                continue
            loaded.append({**s, "representation": s.get("representation", LEGACY_DESIGN)})
    design = _pick_design(sorted({s["representation"] for s in loaded}), design, "strata")

    merged: dict[tuple[float, float], dict[str, Any]] = {}
    for s in loaded:
        if s["representation"] != design:
            continue
        key = (s["band_lo"], s["band_hi"])
        if key in merged:
            if merged[key]["population"] != s["population"]:
                raise SystemExit(
                    f"band {key} has conflicting populations across rounds "
                    f"({merged[key]['population']} vs {s['population']}) — the "
                    f"corpus or embedding changed between draws, so the rounds "
                    f"cannot be pooled.")
            merged[key]["sampled"] += s["sampled"]
        else:
            merged[key] = dict(s)
    return [merged[k] for k in sorted(merged)]


def main() -> None:
    ap = argparse.ArgumentParser(description="Near-dup threshold calibration")
    sp = ap.add_subparsers(dest="cmd", required=True)
    sm = sp.add_parser("sample", help="draw a stratified pair sample and write labelling sheets")
    sm.add_argument("--round", type=int, default=1, choices=sorted(ROUNDS),
                    help="which band schedule to draw (later rounds exclude "
                         "pairs already drawn)")
    design_help = ("representation whose similarity bands the sample was "
                   "stratified on; required once rounds exist under more than "
                   "one, since their band edges are different scales")
    sc = sp.add_parser("score", help="score the labelled rounds of one sampling design")
    sc.add_argument("--design", default=None, help=design_help)
    cp = sp.add_parser("compare", help="re-score existing labels under alternative "
                                       "pair representations")
    cp.add_argument("--reps", nargs="*", default=None,
                    help="representation slugs to compare (default: all)")
    cp.add_argument("--design", default=None, help=design_help)
    cp.add_argument("--fit-n", type=int, default=15000,
                    help="corpus documents used to fit IDF for lexical reps")
    cp.add_argument("--bootstrap", type=int, default=2000,
                    help="stratified bootstrap draws for the CIs (0 to skip)")
    rs = sp.add_parser("reliability-sheet",
                       help="write a blind second-coder sheet for a round")
    rs.add_argument("--round", type=int, default=3, choices=sorted(ROUNDS))
    rs.add_argument("--n", type=int, default=50, help="pairs to double-label")
    rl = sp.add_parser("reliability",
                       help="agreement between the primary and second coder")
    rl.add_argument("--round", type=int, default=3, choices=sorted(ROUNDS))
    args = ap.parse_args()

    cfg = load_config()
    setup_logging(cfg["logging"]["level"])
    outdir = resolve_path(cfg, "reports_dir") / "calibration"

    if args.cmd == "score":
        lab = _labelled_with_context(outdir, args.design)
        design = lab["representation"].iloc[0]
        tbl, bands = score(lab, _merge_strata(outdir, design))
        print(f"\n=== per-band labelled positive rate (stratified on {design}) ===")
        print(bands.to_string(index=False))
        print("\n=== precision / recall by threshold ===")
        print(tbl.to_string(index=False))
        floor = min(b["lo"] for _, b in bands.iterrows())
        print(f"\n(recall is within the >={floor:.2f} {design} candidate pool, "
              f"not absolute)")

        min_p = float(cfg["dedupe"].get("near_dup_min_precision", 0.90))
        op = operating_point(tbl, min_p)
        print(f"\n=== pre-registered operating point (precision >= {min_p:.2f}) ===")
        if op is None:
            print(f"no threshold in this pool reaches precision {min_p:.2f}; the "
                  f"rule selects nothing.\nThat is a finding about the "
                  f"representation, not a reason to lower the floor after the fact.")
        else:
            print(f"threshold {op['threshold']:.3f}  precision {op['precision']:.3f}  "
                  f"recall_in_pool {op['recall_in_pool']:.3f}  "
                  f"retrieves {int(op['pairs_retrieved']):,} pairs")
            print("Rule fixed in config.yaml before any label was seen; the curve "
                  "above is the\nsection-5.3 sensitivity arm, not a menu to pick "
                  "from now.")
        suffix = "" if design == LEGACY_DESIGN else f"_{design}"
        out_p = outdir / f"calibration_results{suffix}.csv"
        out_p.write_text(tbl.to_csv(index=False), encoding="utf-8")
        _LOG.info("wrote %s", out_p)
        return

    if args.cmd in ("reliability-sheet", "reliability"):
        suffix = "" if args.round == 1 else f"_r{args.round}"
        sheet_p = outdir / f"pairs_sample{suffix}.csv"
        if not sheet_p.exists():
            raise SystemExit(f"no {sheet_p.name} — draw the round first")
        sub_p = outdir / RELIABILITY_SHEET.format(suffix=suffix)

        if args.cmd == "reliability-sheet":
            sample = reliability_subset(pd.read_csv(sheet_p), args.n)
            csv_p, html_p, _ = write_sheets(
                sample, [], outdir, suffix,
                csv_name=RELIABILITY_SHEET.format(suffix=suffix),
                html_name=RELIABILITY_HTML.format(suffix=suffix),
                strata_name=None)
            print(f"\n{len(sample)} of the round's pairs, reordered, for a second "
                  f"coder to label blind.\nKeep the two coders apart: agreement is "
                  f"only evidence if the second judgment is independent.\n")
            print(f"  coder 2 labels here : {html_p}")
            print(f"  or edits            : {csv_p}")
            print(f"  then run            : python -m src.dedupe.calibrate "
                  f"reliability --round {args.round}")
            return

        primary = outdir / f"pairs_labelled{suffix}.csv"
        second = outdir / f"reliability_labelled{suffix}.csv"
        for p in (primary, second):
            if not p.exists():
                raise SystemExit(f"missing {p.name} — both coders must have "
                                 f"downloaded their labels")
        st = agreement(pd.read_csv(primary), pd.read_csv(second))
        print(f"\n=== inter-rater agreement, round {args.round} "
              f"({st['n']} doubly-labelled pairs) ===")
        print(f"observed agreement    {st['observed_agreement']:.3f}")
        print(f"Cohen's kappa         {st['cohen_kappa']:.3f}")
        print(f"Krippendorff's alpha  {st['krippendorff_alpha']:.3f}")
        print(f"positives: coder 1 {st['positives_a']}, coder 2 "
              f"{st['positives_b']}; {st['disagreements']} disagreements")
        print("\nConvention in content analysis is alpha >= 0.80 for firm "
              "conclusions and\n>= 0.667 for tentative ones. Report the figure "
              "whatever it is; a low alpha is\nevidence about how well-defined "
              "'same story' is, which is itself a finding.")
        rate = (st["positives_a"] + st["positives_b"]) / (2 * st["n"])
        if min(rate, 1 - rate) < 0.25:
            print(f"\nCaution: only {rate:.0%} of these judgments are positive. "
                  f"With marginals that\nskewed, kappa and alpha are unstable and "
                  f"can read low despite high agreement\n(the prevalence paradox) "
                  f"— quote observed agreement alongside them, and do not\nre-draw "
                  f"the subset to chase a better number.")
        (outdir / f"reliability{suffix}.json").write_text(
            json.dumps(st, indent=2), encoding="utf-8")
        return

    if args.cmd == "compare":
        from src.dedupe import represent

        slugs = args.reps or list(represent.SPECS)
        unknown = [s for s in slugs if s not in represent.SPECS]
        if unknown:
            raise SystemExit(f"unknown representation(s): {', '.join(unknown)}. "
                             f"Available: {', '.join(represent.SPECS)}")
        df = pd.read_parquet(resolve_path(cfg, "articles_parquet"))
        sub = _analysis_subset(df, cfg)
        _LOG.info("analysis-window body-bearing rows: %d", len(sub))
        labelled = _labelled_with_context(outdir, args.design)
        design = labelled["representation"].iloc[0]
        tbl, sims, lab = compare_representations(
            sub, labelled, _merge_strata(outdir, design),
            cfg["dedupe"]["embedding_model"], slugs, fit_n=args.fit_n)

        # The sheet stores each pair's similarity under the design representation,
        # so recomputing that one and comparing verifies the whole url -> row
        # mapping. A mismatch would mean every other representation is scoring the
        # wrong article pairs, and the comparison would be silently meaningless.
        if design in sims:
            drift = float(np.abs(sims[design] - lab["similarity"].to_numpy()).max())
            _LOG.info("%s reproduction check: max |recomputed - stored| = %.6f",
                      design, drift)
            if drift > 0.01:
                raise SystemExit(
                    f"recomputed {design} similarity differs from the stored sample "
                    f"by up to {drift:.4f} — the pair-to-row mapping or the text "
                    f"construction has drifted, so the comparison is not valid.")

        y = lab["label"].to_numpy()
        wt = lab["weight"].to_numpy()
        band_key = lab["band_lo"].to_numpy()
        if args.bootstrap:
            ci, extra = bootstrap_compare(sims, y, wt, band_key, draws=args.bootstrap)
            tbl = tbl.merge(ci, on="representation", how="left")

        print("\n=== representation comparison "
              "(same labels, same weights, same pairs) ===")
        print(tbl.to_string(index=False, float_format=lambda v: f"{v:,.3f}"))
        print(f"\nBaseline = {represent.BASELINE}. AUC/AP are stratum-weighted, so "
              f"they describe the\ncandidate pool of the sampling design "
              f"({design}); 'best_f1' is the peak\nof the weighted F1 curve and is "
              f"selected on the same labels it is scored on,\nso treat it as an "
              f"upper bound.")

        if args.bootstrap:
            winner = tbl.iloc[0]["representation"]
            print(f"\n=== stratified bootstrap ({extra['draws']} draws, resampled "
                  f"within band) ===")
            print(f"est. true pairs in the pool: {extra['est_true_mean']:,.0f}  "
                  f"95% CI [{extra['est_true_lo']:,.0f}, {extra['est_true_hi']:,.0f}]")
            if winner != represent.BASELINE and represent.BASELINE in sims:
                g = paired_gain(sims, y, wt, band_key, winner, represent.BASELINE,
                                draws=args.bootstrap)
                print(f"AP(w) gain, {winner} over baseline: {g['mean']:+.3f}  "
                      f"95% CI [{g['lo']:+.3f}, {g['hi']:+.3f}]   "
                      f"P(gain>0) = {g['p_positive']:.3f}")
            print("\nThe pool-level total is wide because the low bands carry most "
                  "of the pool\nand few labels; the paired gain is narrow because "
                  "both representations are\nscored on the same resampled labels. "
                  "Choosing a representation is therefore\nbetter identified than "
                  "choosing an operating point on it.")

        scores = lab[["pair_id", "label", "weight", "band_lo", "band_hi",
                      "cross_outlet"]].copy()
        for slug, s in sims.items():
            scores[slug] = s
        (outdir / "representation_comparison.csv").write_text(
            tbl.to_csv(index=False), encoding="utf-8")
        scores.to_csv(outdir / "representation_scores.csv", index=False,
                      encoding="utf-8")
        _LOG.info("wrote %s and %s", outdir / "representation_comparison.csv",
                  outdir / "representation_scores.csv")
        return

    bands = ROUNDS[args.round]
    design = ROUND_DESIGN[args.round]
    suffix = "" if args.round == 1 else f"_r{args.round}"
    floor = min(lo for lo, _, _ in bands)
    # Other rounds' sheets are excluded; this round's own is not. Folding in the
    # file this run is about to overwrite would make re-running a round draw a
    # fresh sample disjoint from the one it replaces, so the round could never be
    # reproduced from config — the draw would depend on how many times it had
    # been run before.
    own = f"pairs_sample{suffix}.csv"
    exclude: set[frozenset] = set()
    for p in sorted(outdir.glob("pairs_sample*.csv")):
        if p.name == own:
            continue
        prev = pd.read_csv(p)
        exclude |= {frozenset((a, b)) for a, b in zip(prev["url_a"], prev["url_b"])}
    if exclude:
        _LOG.info("excluding %d pairs drawn in other rounds", len(exclude))

    dd = cfg["dedupe"]
    df = pd.read_parquet(resolve_path(cfg, "articles_parquet"))
    sub = _analysis_subset(df, cfg)
    _LOG.info("analysis-window body-bearing rows: %d", len(sub))
    max_hours = float(dd.get("near_dup_max_hours") or 12)

    # The IDF-fit sample is drawn here, from the subset in its *parquet* order,
    # because that is the order ``compare`` samples in. Fitting on a differently
    # ordered draw of the same size changes the vocabulary and shifts every
    # similarity by ~1e-2 — enough to move pairs across band edges while still
    # looking plausible. The reproduction check below is what catches it.
    fit = sub.sample(n=min(15000, len(sub)), random_state=SEED)

    secs = ((pd.to_datetime(sub["publish_datetime"], format="ISO8601", utc=True)
             - pd.Timestamp("1970-01-01", tz="UTC")) // pd.Timedelta(seconds=1)).to_numpy()
    order = np.argsort(secs, kind="stable")
    sub, secs = sub.iloc[order].reset_index(drop=True), secs[order]

    populations = None
    if design == LEGACY_DESIGN:
        body_chars = int(dd.get("embed_body_chars", 600))
        texts = [((h or "") + ". " + (b or "")[:body_chars]).strip()
                 for h, b in zip(sub["headline"], sub["body"])]
        emb = embed_with_cache(sub["article_id"].tolist(), texts,
                               dd["embedding_model"], body_chars,
                               resolve_path(cfg, "embeddings_cache"))
        I, J, S = candidate_pairs(emb, secs, max_hours, floor=floor)
    else:
        I, J, S, populations = _sparse_pool(
            sub, fit, secs, max_hours, bands, design, exclude,
            outdir / "representation_scores.csv", seed=SEED + args.round)

    sample, strata = draw(sub, I, J, S, bands, seed=SEED + args.round,
                          exclude=exclude, populations=populations, design=design)
    csv_p, html_p, strata_p = write_sheets(sample, strata, outdir, suffix)

    print(f"\n=== round {args.round} strata "
          f"(bands on {design}; population vs sampled) ===")
    print(pd.DataFrame(strata).to_string(index=False))
    print(f"\nsampled {len(sample)} new pairs "
          f"({int(sample['cross_outlet'].sum())} cross-outlet)")
    print(f"\n  label here : {html_p}")
    print(f"  or edit    : {csv_p}  (label column: 1 = same story, 0 = not)")
    print(f"  then run   : python -m src.dedupe.calibrate score --design {design}")
    print(f"               (pools the rounds stratified on {design}; other "
          f"designs' rounds\n               are scored separately, their bands "
          f"being a different scale)")


if __name__ == "__main__":
    main()
