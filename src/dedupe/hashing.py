"""Deduplication.

Phase 1 implements *exact* duplicate detection on the whitespace-normalized body
hash. Clusters are global (across outlets) so verbatim syndication — one wire
story republished unchanged by several outlets — is surfaced directly; that
syndication signal is central to the Phase-4 validity analysis.

Near-duplicate clustering (same story, different wording / light edits) is a
Phase-2 stub: multilingual sentence embeddings + a cosine threshold.
"""
from __future__ import annotations

import logging

import pandas as pd

_LOG = logging.getLogger("vnnews.dedupe")


def assign_exact_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Assign ``dedupe_cluster_id`` per identical body and flag redundant copies.

    Adds/fills:
      - ``dedupe_cluster_id``: 'exact_<n>' for every article that has a body
        (singletons get their own id); None for body-less rows.
      - ``is_exact_duplicate``: True for every copy after the first in a cluster.
    """
    df = df.copy()
    df["dedupe_cluster_id"] = None
    df["is_exact_duplicate"] = False

    mask = df["content_hash"].notna()
    if mask.any():
        sub = df.loc[mask]
        codes, _ = pd.factorize(sub["content_hash"])
        df.loc[mask, "dedupe_cluster_id"] = [f"exact_{c}" for c in codes]
        # First occurrence per identical-content group is canonical; rest are dups.
        order = sub.groupby("content_hash").cumcount()
        df.loc[mask, "is_exact_duplicate"] = order.to_numpy() > 0

    n_dup = int(df["is_exact_duplicate"].sum())
    _LOG.info("exact dedupe: %d redundant copies across %d body-bearing articles",
              n_dup, int(mask.sum()))
    return df


def exact_duplicate_stats(df: pd.DataFrame) -> dict[str, float | int]:
    with_body = int(df["content_hash"].notna().sum())
    dups = int(df.get("is_exact_duplicate", pd.Series(dtype=bool)).sum())
    return {
        "articles_with_body": with_body,
        "exact_duplicate_copies": dups,
        "exact_duplicate_rate": (dups / with_body) if with_body else 0.0,
        "unique_content_clusters": int(df["dedupe_cluster_id"].nunique()),
    }


# Near-duplicate (same-story, embedding-based) clustering now lives in
# ``src.dedupe.near_dup`` and runs as a separate on-demand pass.
