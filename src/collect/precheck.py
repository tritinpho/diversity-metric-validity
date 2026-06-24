"""Pre-flight compliance + liveness check for outlets, before crawling them.

For each candidate outlet this reports, using the *same* robots logic and
User-Agent the crawler uses:

  * whether robots.txt permits our UA to fetch a real article URL and the
    discovery feed/sitemap (catches both explicit disallows and the case where
    our UA token accidentally matches a named-bot rule);
  * any Crawl-delay our UA must honor (the fetcher now enforces
    max(configured, Crawl-delay) per domain);
  * that the discovery source is live and yields article URLs.

Run:  python -m src.collect.precheck
This makes no commitment — it only reports. Encode the green outlets afterwards.
"""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass

from src.collect.discover import _parse_feed, _parse_urlset, _sniff
from src.collect.http import PoliteFetcher
from src.config import ensure_dirs, load_config, setup_logging
from src.utils import url_host

_LOG = logging.getLogger("vnnews.precheck")

# Candidate outlets to vet. Existing three included for a complete record.
# Each: slug, type, homepage, and ordered discovery probes (first live one wins).
CANDIDATES = [
    ("vnexpress",   "semi_commercial",   "https://vnexpress.net",
     ["https://vnexpress.net/rss/thoi-su.rss"]),
    ("tuoitre",     "union_mass_daily",  "https://tuoitre.vn",
     ["https://tuoitre.vn/rss/thoi-su.rss"]),
    ("nhandan",     "party_official",    "https://nhandan.vn",
     ["https://nhandan.vn/sitemaps/google-news.xml"]),
    ("vietnamplus", "party_official",    "https://www.vietnamplus.vn",
     ["https://www.vietnamplus.vn/rss/home.rss",
      "https://www.vietnamplus.vn/sitemaps/google-news.xml"]),
    ("baochinhphu", "party_official",    "https://baochinhphu.vn",
     ["https://baochinhphu.vn/home.rss",
      "https://baochinhphu.vn/sitemaps/google-news.xml"]),
    ("qdnd",        "party_official",    "https://www.qdnd.vn",
     ["https://www.qdnd.vn/sitemaps/0/top300article.xml",
      "https://www.qdnd.vn/sitemaps/pid/feed-0.xml"]),
    ("thanhnien",   "union_mass_daily",  "https://thanhnien.vn",
     ["https://thanhnien.vn/rss/home.rss",
      "https://thanhnien.vn/google-news-sitemap.xml"]),
    ("laodong",     "union_mass_daily",  "https://laodong.vn",
     ["https://laodong.vn/rss/home.rss",
      "https://laodong.vn/google-news-sitemap.xml"]),
    ("tienphong",   "union_mass_daily",  "https://tienphong.vn",
     ["https://tienphong.vn/rss/home.rss",
      "https://tienphong.vn/sitemaps/google-news.xml"]),
    ("vietnamnet",  "semi_commercial",   "https://vietnamnet.vn",
     ["https://vietnamnet.vn/sitemap-news.xml",
      "https://vietnamnet.vn/rss/thoi-su.rss"]),
    ("dantri",      "semi_commercial",   "https://dantri.com.vn",
     ["https://dantri.com.vn/rss/home.rss",
      "https://dantri.com.vn/google-news-sitemap.xml"]),
    ("kenh14",      "popular_lifestyle", "https://kenh14.vn",
     ["https://kenh14.vn/rss/home.rss",
      "https://kenh14.vn/google-news-sitemap.xml"]),
    ("24h",         "popular_lifestyle", "https://www.24h.com.vn",
     ["https://www.24h.com.vn/sitemap-index.xml"]),
    ("soha",        "popular_lifestyle", "https://soha.vn",
     ["https://soha.vn/rss/home.rss",
      "https://soha.vn/google-news-sitemap.xml"]),
    ("saostar",     "popular_lifestyle", "https://www.saostar.vn",
     ["https://www.saostar.vn/rss-feed/tin-moi.rss",
      "https://www.saostar.vn/sitemap-news.xml"]),
    ("cafef",       "sector_business",   "https://cafef.vn",
     ["https://cafef.vn/home.rss",
      "https://cafef.vn/google-news-sitemap.xml"]),
    ("vneconomy",   "sector_business",   "https://vneconomy.vn",
     ["https://vneconomy.vn/sitemap/google-news.xml",
      "https://vneconomy.vn/rss/thoi-su.rss"]),
]


@dataclass
class Result:
    slug: str
    type: str
    discovery: str | None
    n_urls: int
    sample: str | None
    home_ok: bool
    feed_ok: bool
    article_ok: bool
    crawl_delay: float | None
    verdict: str
    note: str = ""


def _first_article(content: bytes, slug: str, otype: str):
    stub = {"slug": slug, "outlet_type": otype}
    kind = _sniff(content)
    if kind == "feed":
        recs = _parse_feed(content, stub, None, "rss")
    elif kind == "urlset":
        recs = _parse_urlset(content, stub)
    else:
        return None, kind, 0
    return (recs[0].url_raw if recs else None), kind, len(recs)


def check(fetcher: PoliteFetcher, slug, otype, home, probes) -> Result:
    home_ok = fetcher.allowed(home)
    cd = fetcher.crawl_delay(home)

    discovery = sample = None
    n_urls = 0
    feed_ok = False
    note = ""
    for probe in probes:
        if not fetcher.allowed(probe):
            note = "robots disallows discovery url"
            continue
        res = fetcher.fetch(probe, kind="feed", force=True)
        if not res.ok or not res.content:
            note = f"discovery fetch failed (HTTP {res.status})"
            continue
        sample, kind, n_urls = _first_article(res.content, slug, otype)
        if sample:
            discovery, feed_ok = probe, True
            break
        note = f"discovery returned no article urls (sniffed {kind})"

    article_ok = bool(sample) and fetcher.allowed(sample)

    if home_ok and feed_ok and article_ok:
        verdict = "OK"
    elif not feed_ok:
        verdict = "NO-DISCOVERY"
    elif not article_ok:
        verdict = "ROBOTS-BLOCKED"
    else:
        verdict = "REVIEW"
    return Result(slug, otype, discovery, n_urls, sample, home_ok, feed_ok,
                  article_ok, cd, verdict, note)


def main() -> None:
    cfg = load_config()
    setup_logging("WARNING")          # quiet; we print our own table
    ensure_dirs(cfg)
    fetcher = PoliteFetcher(cfg)
    print(f"UA: {fetcher.user_agent}\nrespect_robots={fetcher.respect_robots} "
          f"base_rate={fetcher.rate_limit}s\n")

    rows: list[Result] = []
    for slug, otype, home, probes in CANDIDATES:
        rows.append(check(fetcher, slug, otype, home, probes))
        time.sleep(0.5)

    hdr = (f"{'outlet':<12} {'type':<17} {'home':<5} {'feed':<5} {'art':<5} "
           f"{'delay':<6} {'#urls':<6} {'verdict':<14} discovery")
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        print(f"{r.slug:<12} {r.type:<17} "
              f"{'Y' if r.home_ok else 'N':<5} {'Y' if r.feed_ok else 'N':<5} "
              f"{'Y' if r.article_ok else 'N':<5} "
              f"{(str(r.crawl_delay) if r.crawl_delay else '-'):<6} "
              f"{r.n_urls:<6} {r.verdict:<14} "
              f"{(r.discovery or r.note or '')}")

    ok = [r for r in rows if r.verdict == "OK"]
    bad = [r for r in rows if r.verdict != "OK"]
    print(f"\nOK: {len(ok)}/{len(rows)}")
    if bad:
        print("Needs attention: " + ", ".join(f"{r.slug}({r.verdict})" for r in bad))
    delayed = [r for r in rows if r.crawl_delay]
    if delayed:
        print("Crawl-delay declared (honored automatically): "
              + ", ".join(f"{r.slug}={r.crawl_delay}s" for r in delayed))


if __name__ == "__main__":
    main()
