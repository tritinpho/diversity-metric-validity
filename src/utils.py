"""Low-level, dependency-light helpers: URL canonicalization, hashing, text.

Kept free of heavy imports so both ``collect`` and ``normalize`` can use them.
"""
from __future__ import annotations

import hashlib
import re
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

# Query parameters that never identify article content — dropped on canonicalize.
_TRACKING_PARAMS = re.compile(
    r"^(utm_|fbclid$|gclid$|cmpid$|src$|ref$|referrer$|spm$|vn_source|vn_medium|vn_campaign)",
    re.IGNORECASE,
)

_WS = re.compile(r"\s+")


def canonicalize_url(url: str) -> str:
    """Return a canonical form of ``url`` for stable identity / de-duplication.

    - lowercases scheme + host, forces https for known http duplicates
    - drops fragments and tracking query params
    - removes a trailing slash (except on the bare root)
    Article paths on the target outlets are already clean, so this mostly
    normalizes scheme/host casing, strips stray tracking params, and unifies
    the trailing slash.
    """
    url = (url or "").strip()
    if not url:
        return ""
    parts = urlsplit(url)
    scheme = (parts.scheme or "https").lower()
    netloc = parts.netloc.lower()
    # Keep only content-bearing query params, in stable order.
    kept = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=False)
            if not _TRACKING_PARAMS.match(k)]
    query = urlencode(sorted(kept))
    path = parts.path
    if len(path) > 1 and path.endswith("/"):
        path = path.rstrip("/")
    return urlunsplit((scheme, netloc, path, query, ""))


def url_host(url: str) -> str:
    """Return the lowercased host (netloc) for a URL, used as the rate-limit key."""
    return urlsplit(url).netloc.lower()


def make_article_id(canonical_url: str) -> str:
    """Stable article id = first 16 hex chars of sha256(canonical_url)."""
    return hashlib.sha256(canonical_url.encode("utf-8")).hexdigest()[:16]


def normalize_text(text: str | None) -> str:
    """Collapse all whitespace runs to single spaces and strip. '' for None."""
    if not text:
        return ""
    return _WS.sub(" ", text).strip()


def content_hash(body: str | None) -> str | None:
    """Hash of the whitespace-normalized body for exact-duplicate detection.

    None body -> None (no hash, never counts as a duplicate).
    """
    norm = normalize_text(body)
    if not norm:
        return None
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()


def cache_key(url: str) -> str:
    """Filesystem-safe cache key for a URL (sha1 hex)."""
    return hashlib.sha1(url.encode("utf-8")).hexdigest()
