"""Discover article URLs for an outlet: RSS first, sitemap fallback/backfill.

Yields :class:`UrlRecord` objects carrying whatever clean metadata the feed or
sitemap already provides (section, publish datetime, sometimes author), so the
extraction step has a reliable fallback for fields a page might omit.
"""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Iterable

import feedparser
from lxml import etree

from src.collect.http import PoliteFetcher
from src.config import Window
from src.timeutil import parse_dt
from src.utils import canonicalize_url

_LOG = logging.getLogger("vnnews.discover")


@dataclass
class UrlRecord:
    outlet: str
    outlet_type: str
    url_raw: str
    url: str                       # canonical
    section: str | None
    publish_hint: datetime | None  # tz-aware, from feed/sitemap
    source: str                    # 'rss' | 'sitemap'
    author_hint: str | None = None
    title_hint: str | None = None


def _sniff(content: bytes) -> str:
    """Classify XML payload as 'feed' | 'urlset' | 'sitemapindex' | 'unknown'."""
    head = content[:800].lower()
    if b"<rss" in head or b"<feed" in head or b"<item" in head:
        return "feed"
    if b"<sitemapindex" in head:
        return "sitemapindex"
    if b"<urlset" in head:
        return "urlset"
    return "unknown"


def _parse_feed(
    content: bytes, outlet: dict[str, Any], section: str | None, source: str
) -> list[UrlRecord]:
    parsed = feedparser.parse(content)
    out: list[UrlRecord] = []
    for e in parsed.entries:
        link = (e.get("link") or "").strip()
        if not link:
            continue
        hint = parse_dt(e.get("published") or e.get("updated"))
        out.append(UrlRecord(
            outlet=outlet["slug"],
            outlet_type=outlet["outlet_type"],
            url_raw=link,
            url=canonicalize_url(link),
            section=section,
            publish_hint=hint,
            source=source,
            author_hint=(e.get("author") or None),
            title_hint=(e.get("title") or None),
        ))
    return out


def _parse_urlset(content: bytes, outlet: dict[str, Any]) -> list[UrlRecord]:
    """Parse a <urlset> sitemap (incl. Google-News <news:publication_date>)."""
    out: list[UrlRecord] = []
    try:
        root = etree.fromstring(content)
    except etree.XMLSyntaxError as exc:
        _LOG.warning("sitemap XML parse error for %s: %s", outlet["slug"], exc)
        return out
    for url_el in root.findall(".//{*}url"):
        loc_el = url_el.find("{*}loc")
        if loc_el is None or not (loc_el.text or "").strip():
            continue
        link = loc_el.text.strip()
        # Prefer the news publication date, fall back to <lastmod>.
        date_text = None
        news_date = url_el.find(".//{*}news/{*}publication_date")
        if news_date is not None and news_date.text:
            date_text = news_date.text
        else:
            lastmod = url_el.find("{*}lastmod")
            if lastmod is not None and lastmod.text:
                date_text = lastmod.text
        title_el = url_el.find(".//{*}news/{*}title")
        out.append(UrlRecord(
            outlet=outlet["slug"],
            outlet_type=outlet["outlet_type"],
            url_raw=link,
            url=canonicalize_url(link),
            section=None,                  # flat URLs on these outlets -> unknown
            publish_hint=parse_dt(date_text),
            source="sitemap",
            title_hint=(title_el.text if title_el is not None else None),
        ))
    return out


def _child_sitemaps(content: bytes, limit: int) -> list[str]:
    """Return child sitemap locs from a <sitemapindex> (capped)."""
    try:
        root = etree.fromstring(content)
    except etree.XMLSyntaxError:
        return []
    locs = [el.text.strip() for el in root.findall(".//{*}sitemap/{*}loc")
            if el.text and el.text.strip()]
    return locs[:limit]


def _harvest_sitemap(
    url: str, outlet: dict[str, Any], fetcher: PoliteFetcher, *, budget: int, depth: int = 1
) -> list[UrlRecord]:
    # force=True: sitemaps are volatile (new articles appear); always re-poll.
    res = fetcher.fetch(url, kind="feed", force=True)
    if not res.ok or not res.content:
        return []
    kind = _sniff(res.content)
    if kind == "feed":                                   # e.g. Tuoi Tre RSS-sitemap
        return _parse_feed(res.content, outlet, None, "sitemap")
    if kind == "urlset":
        return _parse_urlset(res.content, outlet)
    if kind == "sitemapindex" and depth > 0:
        records: list[UrlRecord] = []
        for child in _child_sitemaps(res.content, limit=5):
            if len(records) >= budget:
                break
            records.extend(_harvest_sitemap(
                child, outlet, fetcher, budget=budget, depth=depth - 1))
        return records
    return []


def _dedupe(records: Iterable[UrlRecord]) -> list[UrlRecord]:
    """Collapse by canonical URL, preferring RSS provenance and richer metadata."""
    by_url: dict[str, UrlRecord] = {}
    for r in records:
        if not r.url:
            continue
        cur = by_url.get(r.url)
        if cur is None:
            by_url[r.url] = r
            continue
        # Merge: fill missing fields; upgrade source to 'rss' if either is rss.
        cur.section = cur.section or r.section
        cur.publish_hint = cur.publish_hint or r.publish_hint
        cur.author_hint = cur.author_hint or r.author_hint
        cur.title_hint = cur.title_hint or r.title_hint
        if r.source == "rss":
            cur.source = "rss"
    return list(by_url.values())


def discover_outlet(
    outlet: dict[str, Any], fetcher: PoliteFetcher, window: Window, cfg: dict[str, Any]
) -> list[UrlRecord]:
    """Return windowed, de-duplicated, capped URL records for one outlet."""
    max_n = cfg["collect"].get("max_articles_per_outlet")
    backfill = bool(cfg["collect"].get("sitemap_backfill", True))
    exclude = [re.compile(p) for p in (outlet.get("exclude_patterns") or [])]

    records: list[UrlRecord] = []
    for feed in outlet.get("rss", []) or []:
        # force=True: RSS "latest" feeds change continuously; always re-poll so
        # daily runs discover new articles (article HTML stays cached downstream).
        res = fetcher.fetch(feed["url"], kind="feed", force=True)
        if not res.ok or not res.content:
            _LOG.warning("[%s] RSS feed unavailable: %s", outlet["slug"], feed["url"])
            continue
        got = _parse_feed(res.content, outlet, feed.get("section"), "rss")
        _LOG.info("[%s] RSS %s -> %d items", outlet["slug"], feed["url"], len(got))
        records.extend(got)

    rss_records = _dedupe(records)
    in_window_rss = [r for r in rss_records if window.contains(r.publish_hint)]

    # Backfill from sitemaps only when RSS did not already meet the cap — this
    # keeps rich-RSS outlets (VnExpress, Tuoi Tre) on RSS alone and lets a
    # thin-RSS outlet (Nhan Dan) top up from its Google-News sitemap.
    need_more = (max_n is None) or (len(in_window_rss) < max_n)
    if backfill and need_more:
        budget = (max_n * 5) if max_n else 2000
        for sm in outlet.get("sitemaps", []) or []:
            if max_n and len([r for r in _dedupe(records)
                              if window.contains(r.publish_hint)]) >= max_n:
                break
            got = _harvest_sitemap(sm, outlet, fetcher, budget=budget)
            _LOG.info("[%s] sitemap %s -> %d urls", outlet["slug"], sm, len(got))
            records.extend(got)

    merged = _dedupe(records)

    # Drop non-article URLs (video, print-edition listings, etc.) before capping.
    if exclude:
        kept = [r for r in merged
                if not any(p.search(r.url_raw) or p.search(r.url) for p in exclude)]
        if len(kept) != len(merged):
            _LOG.info("[%s] excluded %d non-article urls by pattern",
                      outlet["slug"], len(merged) - len(kept))
        merged = kept

    # Window filtering: drop clearly out-of-window items; keep undated ones
    # (their date may resolve from the page) but order them last.
    dated_in = [r for r in merged if window.contains(r.publish_hint)]
    undated = [r for r in merged if r.publish_hint is None]
    dated_in.sort(key=lambda r: r.publish_hint, reverse=True)  # type: ignore[arg-type]
    ordered = dated_in + undated

    if max_n:
        ordered = ordered[:max_n]
    n_dated = sum(1 for r in ordered if r.publish_hint is not None)
    _LOG.info("[%s] selected %d urls (%d dated-in-window, %d undated); "
              "%d dated-in-window available pre-cap",
              outlet["slug"], len(ordered), n_dated, len(ordered) - n_dated, len(dated_in))
    return ordered
