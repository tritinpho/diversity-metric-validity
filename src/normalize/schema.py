"""Map (discovery record + extraction + fetch metadata) onto the target schema.

One row per article, matching the target corpus schema. A few provenance columns
(discovery_source, seg_method, fetch_status) are added for the data-quality
report and debugging; the core fields are exactly those specified for the corpus.
"""
from __future__ import annotations

import html
import logging
import re
import unicodedata
from typing import Any

from langdetect import DetectorFactory, LangDetectException, detect

from src.collect.discover import UrlRecord
from src.collect.http import FetchResult
from src.extract.extract import Extraction
from src.normalize.segment import vi_word_count
from src.timeutil import now, parse_dt, to_iso
from src.utils import canonicalize_url, content_hash, make_article_id

_LOG = logging.getLogger("vnnews.normalize")

# Deterministic language detection (langdetect is randomized by default).
DetectorFactory.seed = 0

# Canonical column order for the corpus.
SCHEMA_COLUMNS = [
    "article_id",
    "outlet",
    "outlet_type",
    "url",
    "url_raw",
    "headline",
    "body",
    "section",
    "publish_datetime",
    "scrape_datetime",
    "author",
    "word_count",
    "lang",
    "content_hash",
    "dedupe_cluster_id",
    # --- provenance (secondary) ---
    "discovery_source",
    "seg_method",
    "fetch_status",
]


# Publication-name tokens trafilatura sometimes prepends to the byline; dropped so
# the author field holds the person, not the outlet. Extend as outlets are added.
_SITE_NAME_TOKENS = {
    "tuoi tre online", "tuoitre", "tuổi trẻ", "tuoi tre",
    "báo nhân dân điện tử", "bao nhan dan dien tu", "nhân dân", "nhandan",
    "vnexpress", "vnexpress.net", "báo điện tử vnexpress",
}
_AUTHOR_SPLIT = re.compile(r"\s*[;|/]\s*|\s+-\s+")


def _strip_symbols(s: str) -> str:
    """Drop symbol/control/format chars (e.g. the ⭐ Tuổi Trẻ appends to bylines).

    Keeps letters, combining marks (essential for Vietnamese), digits, punctuation
    and spaces; removes Unicode symbol (S*) and control/format (Cc/Cf/Co/Cs) chars.
    """
    return "".join(
        c for c in s
        if not (unicodedata.category(c)[0] == "S"
                or unicodedata.category(c) in {"Cc", "Cf", "Co", "Cs"})
    )


def _clean_author(author: str | None) -> str | None:
    """Strip outlet-name tokens and decorative symbols; keep the person name(s)."""
    if not author or not author.strip():
        return None
    author = html.unescape(author)
    parts = [p.strip() for p in _AUTHOR_SPLIT.split(_strip_symbols(author)) if p.strip()]
    kept = [p for p in parts if p.lower() not in _SITE_NAME_TOKENS]
    out = "; ".join(kept) if kept else _strip_symbols(author).strip()
    out = " ".join(out.split())
    return out or None


def _pick_author(record: UrlRecord, extraction: Extraction) -> str | None:
    """Prefer the (clean) RSS author; fall back to a cleaned page byline."""
    return _clean_author(record.author_hint) or _clean_author(extraction.author)


def _clean_text(s: str | None) -> str | None:
    """HTML-unescape and trim a short text field (headline). None-safe."""
    if not s:
        return None
    return html.unescape(s).strip() or None


def _clean_section(section: str | None, headline: str | None) -> str | None:
    """Normalize a section label and drop obvious non-sections.

    Page-derived sections (trafilatura categories) are noisy: HTML entities,
    event/tag names, or even the headline itself. Unescape, then reject a value
    that equals the headline or is sentence-length (> 60 chars) — i.e. not a
    section label. RSS-provided slugs pass through unchanged.
    """
    if not section:
        return None
    s = html.unescape(str(section)).strip()
    if not s or len(s) > 60:
        return None
    if headline and s.casefold() == html.unescape(headline).strip().casefold():
        return None
    return s


def _detect_lang(body: str | None) -> str | None:
    if not body or len(body.strip()) < 20:
        return None
    try:
        return detect(body)
    except LangDetectException:
        return None


def normalize_record(
    record: UrlRecord, extraction: Extraction, fetch: FetchResult
) -> dict[str, Any]:
    """Build one schema row. Always returns a row (missing fields -> None)."""
    canonical = canonicalize_url(fetch.final_url or record.url or record.url_raw)
    body = extraction.body

    # Publish datetime: feed/sitemap hint first (clean, tz-aware), else page metadata.
    publish_dt = record.publish_hint or parse_dt(extraction.date)

    wc, seg_method = vi_word_count(body)
    headline = _clean_text(record.title_hint or extraction.headline)

    return {
        "article_id": make_article_id(canonical),
        "outlet": record.outlet,
        "outlet_type": record.outlet_type,
        "url": canonical,
        "url_raw": record.url_raw,
        "headline": headline,
        "body": body,
        "section": _clean_section(record.section or extraction.section, headline),
        "publish_datetime": to_iso(publish_dt),
        "scrape_datetime": fetch.fetched_at or to_iso(now()),
        "author": _pick_author(record, extraction),
        "word_count": wc if body else None,
        "lang": _detect_lang(body),
        "content_hash": content_hash(body),
        "dedupe_cluster_id": None,           # assigned in the dedupe step
        "discovery_source": record.source,
        "seg_method": seg_method if body else None,
        "fetch_status": fetch.status,
    }
