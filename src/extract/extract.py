"""Article body + metadata extraction via trafilatura.

trafilatura is layout-agnostic and handles all three starter outlets without a
hand-written parser. A per-host override hook is provided for the rare domain
where trafilatura underperforms (none needed yet — add to ``_OVERRIDES``).
"""
from __future__ import annotations

import html
import json
import logging
from dataclasses import dataclass
from typing import Any, Callable

import trafilatura

from src.utils import url_host

_LOG = logging.getLogger("vnnews.extract")


@dataclass
class Extraction:
    body: str | None
    headline: str | None
    author: str | None
    date: str | None       # raw date string from page metadata (resolved later)
    section: str | None    # from page categories/tags, if any
    ok: bool


def _first_category(data: dict[str, Any]) -> str | None:
    """Pull a single section-ish label from trafilatura categories/tags.

    HTML entities are resolved *before* splitting on separators — some outlets
    (e.g. vneconomy) encode Vietnamese diacritics as ``&#x1EC7;`` whose internal
    ``;`` would otherwise split the label mid-character and truncate it.
    """
    for key in ("categories", "tags"):
        val = data.get(key)
        if not val:
            continue
        if isinstance(val, list):
            for item in val:
                s = html.unescape(str(item)).strip() if item else ""
                if s:
                    return s
        elif isinstance(val, str):
            first = html.unescape(val).replace(";", ",").split(",")[0].strip()
            if first:
                return first
    return None


def _run_trafilatura(content: bytes | str, url: str) -> dict[str, Any] | None:
    """Call trafilatura.extract -> parsed JSON dict, tolerant of version differences."""
    kwargs = dict(
        url=url,
        output_format="json",
        include_comments=False,
        include_tables=False,
        with_metadata=True,
    )
    try:
        js = trafilatura.extract(content, favor_precision=True, **kwargs)
    except TypeError:
        # Older/newer signature without favor_precision.
        js = trafilatura.extract(content, **kwargs)
    if not js:
        return None
    try:
        return json.loads(js)
    except json.JSONDecodeError:
        return None


# host -> function(content, url, extraction) -> Extraction  (post-processing hook)
_OVERRIDES: dict[str, Callable[[bytes, str, "Extraction"], "Extraction"]] = {}


def extract_article(content: bytes | None, url: str) -> Extraction:
    """Extract clean main text + metadata for a single article page."""
    if not content:
        return Extraction(None, None, None, None, None, ok=False)

    data = _run_trafilatura(content, url)
    if not data:
        _LOG.debug("trafilatura returned nothing for %s", url)
        return Extraction(None, None, None, None, None, ok=False)

    body = (data.get("text") or "").strip() or None
    extraction = Extraction(
        body=body,
        headline=(data.get("title") or "").strip() or None,
        author=(data.get("author") or "").strip() or None,
        date=(data.get("date") or "").strip() or None,
        section=_first_category(data),
        ok=body is not None,
    )

    override = _OVERRIDES.get(url_host(url))
    if override is not None:
        extraction = override(content, url, extraction)
    return extraction
