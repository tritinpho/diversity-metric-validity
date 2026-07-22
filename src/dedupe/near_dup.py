"""Embedding-based near-duplicate / same-story clustering (Phase 2).

Exact content-hash dedup (see ``hashing.py``) only catches *verbatim* copies.
Most "same story across outlets" is lightly reworded — shared wire copy, edited
headlines, trimmed bodies. This pass embeds each article with a multilingual
sentence encoder and links articles whose cosine similarity exceeds a threshold
into near-duplicate clusters (connected components), spanning outlets.

Two things stop the connected components from over-merging:

*Temporal constraint.* A cosine threshold alone is not enough. Vietnamese online
news carries a lot of recurring templated genres — daily gold- and petrol-price
columns, match-fixture and lottery lists — where today's article is >=0.94
similar to the same column published tomorrow. Under single linkage that chains
a whole month into one cluster (observed on this corpus: 189 articles across 14
outlets, all gold-price columns). Only pairs published within
``dedupe.near_dup_max_hours`` of each other are linked; genuine syndication is
same-day, so the constraint cuts the chains while still catching copies that
straddle midnight.

*Cached embeddings.* Embedding the corpus is the expensive step, and it does not
depend on the threshold or the time window. Vectors are cached to
``paths.embeddings_cache``, keyed by (model, ``embed_body_chars``), so a
threshold/window sweep re-clusters in seconds instead of re-embedding::

    python -m src.dedupe.near_dup                      # cluster + write back + summary
    python -m src.dedupe.near_dup --threshold 0.92     # re-uses cached vectors
    python -m src.dedupe.near_dup --max-hours 24 --dry-run
    python -m src.dedupe.near_dup --refresh-embeddings # force re-embed

Similarity is computed in row-blocks rather than as one n x n matrix (which
would be ~9GB at 48k articles). With a time constraint each block only needs the
columns inside its window, so the blocks stay small.
"""
from __future__ import annotations

import argparse
import logging
import os
from pathlib import Path

import numpy as np
import pandas as pd

from src.config import load_config, resolve_path, setup_logging

# Fail fast on a stalled model download instead of hanging indefinitely (the
# huggingface_hub default has no read timeout). A cached model is unaffected.
os.environ.setdefault("HF_HUB_DOWNLOAD_TIMEOUT", "30")

_LOG = logging.getLogger("vnnews.neardup")

_MODEL = None


def _model(name: str):
    """Lazy-load the sentence-transformer (downloaded once, then cached)."""
    global _MODEL
    if _MODEL is None:
        from sentence_transformers import SentenceTransformer
        _LOG.info("loading embedding model: %s", name)
        _MODEL = SentenceTransformer(name)
    return _MODEL


def embed_texts(texts: list[str], model_name: str, batch_size: int = 32) -> np.ndarray:
    """Return L2-normalized float32 embeddings for ``texts``."""
    model = _model(model_name)
    emb = model.encode(texts, batch_size=batch_size, convert_to_numpy=True,
                       normalize_embeddings=True, show_progress_bar=False)
    return emb.astype("float32")


# ------------------------------------------------------------ embedding cache
def _cache_load(
    path: Path | None, model_name: str, body_chars: int
) -> tuple[dict[str, int], np.ndarray | None]:
    """Load cached vectors as ``(article_id -> row index, matrix)``.

    The cache is only valid for the (model, body_chars) pair it was built with —
    a different encoder or a different amount of body text yields different
    vectors, so a mismatch is discarded rather than silently mixed.
    """
    if path is None or not path.exists():
        return {}, None
    try:
        z = np.load(path, allow_pickle=False)
        if str(z["model"]) != model_name or int(z["body_chars"]) != int(body_chars):
            _LOG.warning(
                "embedding cache was built with model=%s body_chars=%s "
                "(now %s / %s) -> ignoring cache",
                z["model"], z["body_chars"], model_name, body_chars)
            return {}, None
        ids, emb = z["article_ids"], z["embeddings"]
        _LOG.info("embedding cache: %d vectors at %s", len(ids), path)
        return {a: i for i, a in enumerate(ids.tolist())}, emb
    except Exception as exc:  # corrupt/partial file must not kill the run
        _LOG.warning("could not read embedding cache (%s) -> ignoring", exc)
        return {}, None


def _cache_save(
    path: Path | None, model_name: str, body_chars: int,
    article_ids: list[str], emb: np.ndarray,
    prev_idx: dict[str, int], prev_emb: np.ndarray | None,
) -> None:
    """Write the union of previously cached and freshly computed vectors."""
    if path is None:
        return
    ids, mat = list(article_ids), [emb]
    if prev_emb is not None and len(prev_idx):
        keep = [a for a in prev_idx if a not in set(article_ids)]
        if keep:
            ids += keep
            mat.append(prev_emb[[prev_idx[a] for a in keep]])
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez(path, article_ids=np.array(ids), embeddings=np.vstack(mat),
             model=np.array(model_name), body_chars=np.array(int(body_chars)))
    _LOG.info("embedding cache: wrote %d vectors -> %s", len(ids), path)


def embed_with_cache(
    article_ids: list[str], texts: list[str], model_name: str,
    body_chars: int, cache_path: Path | None, batch_size: int = 32,
) -> np.ndarray:
    """Embeddings for ``texts``, computing only the ones not already cached."""
    prev_idx, prev_emb = _cache_load(cache_path, model_name, body_chars)
    missing = [i for i, a in enumerate(article_ids) if a not in prev_idx]
    _LOG.info("embeddings: %d cached, %d to compute",
              len(article_ids) - len(missing), len(missing))

    fresh = embed_texts([texts[i] for i in missing], model_name, batch_size) \
        if missing else None
    dim = fresh.shape[1] if fresh is not None else prev_emb.shape[1]

    out = np.empty((len(article_ids), dim), dtype="float32")
    for i, a in enumerate(article_ids):
        j = prev_idx.get(a)
        if j is not None:
            out[i] = prev_emb[j]
    if fresh is not None:
        out[missing] = fresh
        _cache_save(cache_path, model_name, body_chars, article_ids, out,
                    prev_idx, prev_emb)
    return out


# ---------------------------------------------------------------- clustering
def cluster_near_dups(
    embeddings: np.ndarray, threshold: float,
    timestamps: np.ndarray | None = None, max_hours: float | None = None,
    block_size: int = 4000,
) -> list[int]:
    """Connected-component clustering over cosine similarity >= threshold.

    ``embeddings`` must be L2-normalized so that the dot product is cosine.
    Returns a contiguous cluster label (0..k-1) per row; singletons get their
    own label. Pure-numpy union-find, so it is unit-testable without the model.

    If ``timestamps`` (int64 seconds, **sorted ascending**, one per row) and
    ``max_hours`` are given, two rows are only linked when they were published
    within ``max_hours`` of each other. This is what stops recurring templated
    articles from chaining across days — see the module docstring.

    Similarity is computed in row-blocks rather than materializing the full
    n x n matrix (~9GB+ at 48k articles). Each block compares row i only
    against columns j > i, so results are identical to the single-matrix
    version; under a time constraint the columns stop at the window edge too.
    """
    n = len(embeddings)
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    bounded = timestamps is not None and max_hours is not None
    if bounded:
        ts = np.asarray(timestamps, dtype="int64")
        if len(ts) != n:
            raise ValueError(f"timestamps has {len(ts)} rows, embeddings has {n}")
        if np.any(np.diff(ts) < 0):
            raise ValueError("timestamps must be sorted ascending")
        # hi[i] = first row index outside i's forward window (exclusive bound).
        hi = np.searchsorted(ts, ts + int(max_hours * 3600), side="right")
        # A window that reaches most of the corpus means the constraint is inert
        # — almost always a timestamp-unit error rather than a real result.
        reach = int(np.median(hi - np.arange(n)))
        _LOG.info("time window: %gh -> median %d candidate rows ahead (n=%d)",
                  max_hours, reach, n)
        if n > 100 and reach > n // 2:
            _LOG.warning("time constraint is barely binding (median reach %d of "
                         "%d rows) — check that timestamps are in SECONDS", reach, n)
    else:
        hi = np.full(n, n, dtype="int64")

    for start in range(0, n - 1, block_size):
        end = min(start + block_size, n)
        # hi is non-decreasing (ts sorted), so the block's widest reach is its last row.
        hi_max = int(hi[end - 1])
        if hi_max <= start + 1:
            continue
        sim = embeddings[start:end] @ embeddings[start:hi_max].T
        rows = np.arange(start, end)[:, None]
        cols = np.arange(start, hi_max)[None, :]
        linked = sim >= threshold
        linked &= cols > rows
        if bounded:
            linked &= cols < hi[start:end][:, None]
        for bi, bj in np.argwhere(linked):
            union(start + int(bi), start + int(bj))

    remap: dict[int, int] = {}
    labels = []
    for i in range(n):
        root = find(i)
        if root not in remap:
            remap[root] = len(remap)
        labels.append(remap[root])
    return labels


def assign_near_duplicates(
    df: pd.DataFrame, threshold: float, model_name: str, body_chars: int = 600,
    max_hours: float | None = None, cache_path: Path | None = None,
) -> pd.DataFrame:
    """Add ``near_dup_cluster_id`` / ``is_near_duplicate`` / ``near_dup_cluster_size``.

    Only body-bearing rows are embedded and clustered; body-less rows get null
    cluster ids. Within a cluster the first row (corpus order) is canonical.
    """
    df = df.copy()
    df["near_dup_cluster_id"] = None
    df["is_near_duplicate"] = False
    df["near_dup_cluster_size"] = 1

    mask = df["body"].notna()
    sub = df[mask]
    if sub.empty:
        _LOG.warning("no body-bearing rows to cluster")
        return df

    texts = [((h or "") + ". " + (b or "")[:body_chars]).strip()
             for h, b in zip(sub["headline"], sub["body"])]
    emb = embed_with_cache(sub["article_id"].tolist(), texts, model_name,
                           body_chars, cache_path)

    if max_hours is None:
        labels = np.asarray(cluster_near_dups(emb, threshold), dtype="int64")
    else:
        ts = pd.to_datetime(sub["publish_datetime"], format="ISO8601",
                            utc=True, errors="coerce")
        datable = ts.notna().to_numpy()
        if not datable.all():
            _LOG.warning("%d body-bearing rows have no parseable publish_datetime; "
                         "leaving them as singletons under the time constraint",
                         int((~datable).sum()))
        # Cluster in time order so the forward window is a contiguous row range.
        # Convert via Timedelta rather than astype("int64"): pandas picks the
        # datetime resolution from the data (this corpus parses as us, not ns),
        # so a hardcoded divisor silently scales every timestamp and turns the
        # window into a no-op. Only datable rows are converted — NaT would
        # astype to the int64 sentinel, a valid-looking timestamp in 1677.
        secs = np.zeros(len(sub), dtype="int64")
        secs[datable] = ((ts[datable] - pd.Timestamp("1970-01-01", tz="UTC"))
                         // pd.Timedelta(seconds=1)).to_numpy()
        order = np.flatnonzero(datable)
        order = order[np.argsort(secs[order], kind="stable")]
        _LOG.info("clustering %d articles at cosine>=%.2f within +/-%gh",
                  len(order), threshold, max_hours)
        sorted_labels = cluster_near_dups(emb[order], threshold,
                                          timestamps=secs[order], max_hours=max_hours)
        labels = np.full(len(sub), -1, dtype="int64")
        labels[order] = sorted_labels
        # Undatable rows cannot be time-checked, so they stay singletons.
        loose = np.flatnonzero(labels < 0)
        labels[loose] = labels.max() + 1 + np.arange(len(loose))

    # Renumber by first appearance in corpus order so ids read in corpus order.
    _, first = np.unique(labels, return_index=True)
    remap = {old: new for new, old in enumerate(labels[np.sort(first)])}
    ids = pd.Series([f"near_{remap[int(l)]}" for l in labels], index=sub.index)

    df.loc[mask, "near_dup_cluster_id"] = ids
    df.loc[mask, "near_dup_cluster_size"] = ids.map(ids.value_counts()).to_numpy()
    df.loc[mask, "is_near_duplicate"] = ids.groupby(ids).cumcount().to_numpy() > 0
    return df


def summarize(df: pd.DataFrame) -> dict[str, int]:
    bodied = df[df["near_dup_cluster_id"].notna()]
    clusters = bodied.groupby("near_dup_cluster_id")
    sizes = clusters.size()
    multi = sizes[sizes > 1]
    cross = clusters["outlet"].nunique()
    cross_ids = cross[cross > 1].index
    out = {
        "articles": int(len(bodied)),
        "near_dup_clusters_multi": int(len(multi)),
        "near_dup_copies": int(df["is_near_duplicate"].sum()),
        "largest_cluster": int(sizes.max()) if len(sizes) else 0,
        "cross_outlet_clusters": int(len(cross_ids)),
        "articles_in_cross_outlet": int(bodied["near_dup_cluster_id"].isin(cross_ids).sum()),
    }
    # Chaining check: a same-story cluster should not span days (see docstring).
    if "publish_datetime" in bodied.columns:
        day = pd.to_datetime(bodied["publish_datetime"], format="ISO8601",
                             utc=True, errors="coerce").dt.tz_convert(
                                 "Asia/Ho_Chi_Minh").dt.normalize()
        spans = day.groupby(bodied["near_dup_cluster_id"]).agg(lambda s: (s.max() - s.min()).days)
        out["multi_day_clusters"] = int((spans.loc[multi.index] > 1).sum()) if len(multi) else 0
        out["max_cluster_span_days"] = int(spans.max()) if len(spans) else 0
    return out


def _print_cross_outlet(df: pd.DataFrame, limit: int = 12) -> None:
    bodied = df[df["near_dup_cluster_id"].notna()]
    nout = bodied.groupby("near_dup_cluster_id")["outlet"].nunique()
    cross = nout[nout > 1].sort_values(ascending=False).index[:limit]
    print(f"\n=== sample cross-outlet same-story clusters (top {len(cross)}) ===")
    for cid in cross:
        c = df[df["near_dup_cluster_id"] == cid]
        outs = ", ".join(sorted(c["outlet"].unique()))
        print(f"\n[{cid}]  outlets: {outs}")
        for _, r in c.iterrows():
            print(f"   {r.outlet:<11} {str(r.headline)[:80]}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Near-duplicate / same-story clustering")
    ap.add_argument("--threshold", type=float, default=None,
                    help="cosine threshold (overrides config)")
    ap.add_argument("--max-hours", type=float, default=None,
                    help="only link articles published within N hours "
                         "(overrides config; 0 disables the constraint)")
    ap.add_argument("--refresh-embeddings", action="store_true",
                    help="ignore the embedding cache and re-embed from scratch")
    ap.add_argument("--dry-run", action="store_true",
                    help="cluster + summarize but do not write back")
    args = ap.parse_args()

    cfg = load_config()
    setup_logging(cfg["logging"]["level"])
    dd = cfg["dedupe"]
    threshold = args.threshold if args.threshold is not None else float(dd["near_dup_threshold"])
    raw_hours = args.max_hours if args.max_hours is not None else dd.get("near_dup_max_hours")
    max_hours = None if raw_hours in (None, 0) else float(raw_hours)

    parquet = resolve_path(cfg, "articles_parquet")
    if not parquet.exists():
        raise SystemExit(f"no corpus at {parquet}")
    try:
        cache_path = resolve_path(cfg, "embeddings_cache")
    except KeyError:
        cache_path = None
    if args.refresh_embeddings and cache_path and cache_path.exists():
        cache_path.unlink()
        _LOG.info("removed embedding cache -> re-embedding from scratch")

    df = pd.read_parquet(parquet)
    _LOG.info("loaded %d articles; clustering at cosine>=%.2f, window=%s",
              len(df), threshold, f"{max_hours}h" if max_hours else "unconstrained")
    df = assign_near_duplicates(df, threshold, dd["embedding_model"],
                                int(dd.get("embed_body_chars", 600)),
                                max_hours=max_hours, cache_path=cache_path)

    stats = summarize(df)
    print(f"\n====== NEAR-DUP SUMMARY (threshold={threshold}, "
          f"max_hours={max_hours}) ======")
    for k, v in stats.items():
        print(f"{k:<28} {v}")
    print("=" * 64)
    _print_cross_outlet(df)

    if not args.dry_run:
        df.to_parquet(parquet, index=False)
        _LOG.info("wrote near-dup columns back -> %s", parquet)
    else:
        _LOG.info("dry-run: corpus not modified")


if __name__ == "__main__":
    main()
