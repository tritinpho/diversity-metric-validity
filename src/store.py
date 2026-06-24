"""Corpus persistence: load + incremental merge.

A single run captures only the latest cross-section (RSS "latest" feeds ≈ the
last couple of days). The project target is a 2–4 week window, so runs must
*accumulate*: each run's rows are merged into the existing corpus and de-duped
by ``article_id`` (an article re-seen on a later day is kept once, newest scrape
winning). This is what lets a daily snapshot fill the window over time.
"""
from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

_LOG = logging.getLogger("vnnews.store")


def load_corpus(path: str | Path) -> pd.DataFrame | None:
    """Load the existing corpus, or None if it does not exist yet."""
    p = Path(path)
    if not p.exists():
        return None
    return pd.read_parquet(p)


def merge_corpus(existing: pd.DataFrame | None, new_df: pd.DataFrame) -> pd.DataFrame:
    """Union ``new_df`` into ``existing`` and de-dupe by ``article_id``.

    Newest scrape wins on collision (handles re-extraction/edits). Returns the
    merged frame; dedupe-cluster columns are recomputed by the caller afterwards.
    """
    if existing is None or existing.empty:
        combined = new_df.copy()
    else:
        combined = pd.concat([existing, new_df], ignore_index=True)
    if "scrape_datetime" in combined.columns:
        combined = combined.sort_values("scrape_datetime", na_position="first")
    combined = combined.drop_duplicates(subset="article_id", keep="last")
    return combined.reset_index(drop=True)
