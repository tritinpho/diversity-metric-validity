"""Polite, cached HTTP fetching.

A single :class:`PoliteFetcher` enforces the project's polite-citizen rules:

* respects ``robots.txt`` (via :mod:`urllib.robotparser`, cached per host);
* rate-limits per domain with jitter (so re-runs and multiple feeds don't burst);
* caches every response to disk so re-runs never re-hit the origin (resumable);
* retries transient errors (429 / 5xx / network) with exponential backoff;
* sends a descriptive User-Agent with a contact address.

Cache layout (keyed by sha1 of the requested URL)::

    data/raw/html/<key>.html   + <key>.meta.json     # article pages
    data/raw/feeds/<key>.xml   + <key>.meta.json     # RSS / sitemaps
"""
from __future__ import annotations

import json
import logging
import random
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.robotparser import RobotFileParser

import requests
from tenacity import (
    Retrying,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)

from src.config import resolve_path
from src.timeutil import now, to_iso
from src.utils import cache_key, url_host

_LOG = logging.getLogger("vnnews.http")


class _RetryableHTTP(Exception):
    """Raised on 429/5xx so tenacity retries with backoff."""


@dataclass
class FetchResult:
    url: str
    final_url: str
    status: int
    content: bytes | None
    from_cache: bool
    ok: bool
    error: str | None = None
    fetched_at: str | None = None


class PoliteFetcher:
    def __init__(self, cfg: dict[str, Any]) -> None:
        h = cfg["http"]
        self.user_agent: str = h["user_agent"]
        self.timeout: float = float(h["timeout_seconds"])
        self.rate_limit: float = float(h["rate_limit_seconds"])
        self.jitter: float = float(h["rate_limit_jitter_seconds"])
        self.max_retries: int = int(h["max_retries"])
        self.backoff_base: float = float(h["backoff_base_seconds"])
        self.backoff_max: float = float(h.get("backoff_max_seconds", 30.0))
        self.respect_robots: bool = bool(h.get("respect_robots", True))

        self.html_dir: Path = resolve_path(cfg, "raw_html")
        self.feeds_dir: Path = resolve_path(cfg, "raw_feeds")
        self.robots_dir: Path = resolve_path(cfg, "robots_cache")

        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": self.user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml,"
                      "application/rss+xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "vi,en;q=0.8",
        })

        self._last_request: dict[str, float] = {}     # host -> monotonic ts
        self._robots: dict[str, RobotFileParser | None] = {}

        # Counters surfaced in the run summary.
        self.stats = {"fetched": 0, "cache_hits": 0, "errors": 0, "robots_blocked": 0}

    # ------------------------------------------------------------------ robots
    def _robots_for(self, host: str) -> RobotFileParser | None:
        """Return a parsed RobotFileParser for ``host`` (cached), or None to allow.

        404 / parse-empty -> permissive (None means 'no restrictions'). Network or
        5xx error fetching robots -> permissive + warning (don't halt collection on
        a flaky robots endpoint), which mirrors common crawler behaviour.
        """
        if host in self._robots:
            return self._robots[host]
        url = f"https://{host}/robots.txt"
        rp: RobotFileParser | None = None
        try:
            resp = self.session.get(url, timeout=self.timeout)
            if resp.status_code == 200 and resp.text.strip():
                rp = RobotFileParser()
                rp.parse(resp.text.splitlines())
                (self.robots_dir / f"{host}.txt").write_text(resp.text, encoding="utf-8")
            else:
                _LOG.info("robots.txt for %s -> HTTP %s; treating as permissive",
                          host, resp.status_code)
        except requests.RequestException as exc:
            _LOG.warning("robots.txt fetch failed for %s (%s); treating as permissive",
                         host, exc)
        self._robots[host] = rp
        return rp

    def allowed(self, url: str) -> bool:
        if not self.respect_robots:
            return True
        rp = self._robots_for(url_host(url))
        if rp is None:
            return True
        return rp.can_fetch(self.user_agent, url)

    def crawl_delay(self, url: str) -> float | None:
        """Robots-declared Crawl-delay for our UA on this host (None if unset)."""
        rp = self._robots_for(url_host(url))
        if rp is None:
            return None
        try:
            cd = rp.crawl_delay(self.user_agent)
            return float(cd) if cd is not None else None
        except Exception:  # pragma: no cover - robotparser edge cases
            return None

    # -------------------------------------------------------------- rate limit
    def _host_min_delay(self, host: str) -> float:
        """Per-request delay = max(configured rate limit, robots Crawl-delay)."""
        rp = self._robots.get(host)
        cd = None
        if rp is not None:
            try:
                cd = rp.crawl_delay(self.user_agent)
            except Exception:  # pragma: no cover
                cd = None
        return max(self.rate_limit, float(cd or 0.0))

    def _throttle(self, host: str) -> None:
        last = self._last_request.get(host)
        if last is not None:
            wait = self._host_min_delay(host) - (time.monotonic() - last)
            wait += random.uniform(0, self.jitter)
            if wait > 0:
                time.sleep(wait)
        self._last_request[host] = time.monotonic()

    # ------------------------------------------------------------------- cache
    def _paths(self, url: str, kind: str) -> tuple[Path, Path]:
        base = self.feeds_dir if kind == "feed" else self.html_dir
        ext = "xml" if kind == "feed" else "html"
        key = cache_key(url)
        return base / f"{key}.{ext}", base / f"{key}.meta.json"

    def _read_cache(self, url: str, kind: str) -> FetchResult | None:
        content_path, meta_path = self._paths(url, kind)
        if not (content_path.exists() and meta_path.exists()):
            return None
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            content = content_path.read_bytes()
        except (OSError, json.JSONDecodeError):
            return None
        return FetchResult(
            url=url,
            final_url=meta.get("final_url", url),
            status=int(meta.get("status", 200)),
            content=content,
            from_cache=True,
            ok=bool(meta.get("ok", True)),
            fetched_at=meta.get("fetched_at"),
        )

    def _write_cache(self, url: str, kind: str, resp: requests.Response) -> str:
        content_path, meta_path = self._paths(url, kind)
        fetched = to_iso(now())
        content_path.write_bytes(resp.content)
        meta_path.write_text(json.dumps({
            "requested_url": url,
            "final_url": resp.url,
            "status": resp.status_code,
            "content_type": resp.headers.get("Content-Type", ""),
            "ok": resp.status_code == 200,
            "fetched_at": fetched,
        }, ensure_ascii=False, indent=2), encoding="utf-8")
        return fetched

    # ------------------------------------------------------------------- fetch
    def _get_with_retry(self, url: str) -> requests.Response:
        retryer = Retrying(
            stop=stop_after_attempt(self.max_retries),
            wait=wait_random_exponential(multiplier=self.backoff_base, max=self.backoff_max),
            retry=retry_if_exception_type((requests.RequestException, _RetryableHTTP)),
            reraise=True,
        )

        def _do() -> requests.Response:
            resp = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            if resp.status_code == 429 or resp.status_code >= 500:
                raise _RetryableHTTP(f"HTTP {resp.status_code}")
            return resp

        return retryer(_do)

    def fetch(self, url: str, kind: str = "html", force: bool = False) -> FetchResult:
        """Fetch ``url`` (kind in {'html','feed'}), using the disk cache when possible."""
        if not force:
            cached = self._read_cache(url, kind)
            if cached is not None:
                self.stats["cache_hits"] += 1
                return cached

        if not self.allowed(url):
            self.stats["robots_blocked"] += 1
            _LOG.warning("robots.txt disallows %s; skipping", url)
            return FetchResult(url, url, 0, None, False, ok=False, error="robots-disallowed")

        self._throttle(url_host(url))
        try:
            resp = self._get_with_retry(url)
        except (requests.RequestException, _RetryableHTTP) as exc:
            self.stats["errors"] += 1
            _LOG.warning("fetch failed: %s (%s)", url, exc)
            return FetchResult(url, url, 0, None, False, ok=False, error=str(exc))

        ok = resp.status_code == 200
        if ok:
            fetched = self._write_cache(url, kind, resp)
            self.stats["fetched"] += 1
        else:
            self.stats["errors"] += 1
            fetched = to_iso(now())
            _LOG.warning("non-200 for %s -> HTTP %s", url, resp.status_code)
        return FetchResult(
            url=url,
            final_url=resp.url,
            status=resp.status_code,
            content=resp.content if ok else None,
            from_cache=False,
            ok=ok,
            fetched_at=fetched,
        )
