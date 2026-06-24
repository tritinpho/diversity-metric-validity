"""Embedding-based near-duplicate / same-story clustering (Phase 2).

Exact content-hash dedup (see ``hashing.py``) only catches *verbatim* copies.
Most "same story across outlets" is lightly reworded — shared wire copy, edited
headlines, trimmed bodies. This pass embeds each article with a multilingual
sentence encoder and links articles whose cosine similarity exceeds a threshold
into near-duplicate clusters (connected components), spanning outlets.

It is a *separate, on-demand* pass — embedding the whole corpus is far heavier
than collection and need not run on every crawl::

    python -m src.dedupe.near_dup                 # cluster + write back + summary
    python -m src.dedupe.near_dup --threshold 0.8

Clustering is O(n^2) in the corpus size (fine for the current snapshot; block or
approximate-NN if the corpus grows past tens of thousands).
"""
from __future__ import annotations

import argparse
import logging
from pathlib import Path

import numpy as np
import pandas as pd

from src.config import load_config, resolve_path, setup_logging

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


def cluster_near_dups(embeddings: np.ndarray, threshold: float) -> list[int]:
    """Connected-component clustering over cosine similarity >= threshold.

    ``embeddings`` must be L2-normalized so that the dot product is cosine.
    Returns a contiguous cluster label (0..k-1) per row; singletons get their
    own label. Pure-numpy union-find, so it is unit-testable without the model.
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

    if n > 1:
        sim = embeddings @ embeddings.T
        for i, j in np.argwhere(np.triu(sim >= threshold, k=1)):
            union(int(i), int(j))

    remap: dict[int, int] = {}
    labels = []
    for i in range(n):
        root = find(i)
        if root not in remap:
            remap[root] = len(remap)
        labels.append(remap[root])
    return labels


def assign_near_duplicates(
    df: pd.DataFrame, threshold: float, model_name: str, body_chars: int = 600
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
    _LOG.info("embedding %d articles", len(texts))
    emb = embed_texts(texts, model_name)
    labels = cluster_near_dups(emb, threshold)
    ids = [f"near_{l}" for l in labels]

    sizes = pd.Series(ids).value_counts()
    df.loc[mask, "near_dup_cluster_id"] = ids
    df.loc[mask, "near_dup_cluster_size"] = [int(sizes[i]) for i in ids]
    df.loc[mask, "is_near_duplicate"] = pd.Series(ids).groupby(ids).cumcount().to_numpy() > 0
    return df


def summarize(df: pd.DataFrame) -> dict[str, int]:
    bodied = df[df["near_dup_cluster_id"].notna()]
    clusters = bodied.groupby("near_dup_cluster_id")
    multi = clusters.size()[clusters.size() > 1]
    cross = clusters["outlet"].nunique()
    cross_ids = cross[cross > 1].index
    return {
        "articles": int(len(bodied)),
        "near_dup_clusters_multi": int(len(multi)),
        "near_dup_copies": int(df["is_near_duplicate"].sum()),
        "cross_outlet_clusters": int(len(cross_ids)),
        "articles_in_cross_outlet": int(bodied["near_dup_cluster_id"].isin(cross_ids).sum()),
    }


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
    ap.add_argument("--dry-run", action="store_true",
                    help="cluster + summarize but do not write back")
    args = ap.parse_args()

    cfg = load_config()
    setup_logging(cfg["logging"]["level"])
    dd = cfg["dedupe"]
    threshold = args.threshold if args.threshold is not None else float(dd["near_dup_threshold"])
    parquet = resolve_path(cfg, "articles_parquet")
    if not parquet.exists():
        raise SystemExit(f"no corpus at {parquet}")

    df = pd.read_parquet(parquet)
    _LOG.info("loaded %d articles; clustering at cosine>=%.2f", len(df), threshold)
    df = assign_near_duplicates(df, threshold, dd["embedding_model"],
                                int(dd.get("embed_body_chars", 600)))

    stats = summarize(df)
    print(f"\n================ NEAR-DUP SUMMARY (threshold={threshold}) ========")
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
