"""Offline smoke tests for the pure logic (no network).

Run either way:
    python -m pytest tests/test_smoke.py
    python tests/test_smoke.py          # self-contained runner, no pytest needed
"""
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

# Make ``src`` importable when run directly.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
import pandas as pd

from src.config import resolve_window, load_config
from src.dedupe.hashing import assign_exact_duplicates, exact_duplicate_stats
from src.dedupe.near_dup import cluster_near_dups
from src.collect.discover import _parse_feed, _parse_urlset, _sniff
from src.extract.extract import _first_category
from src.normalize.schema import _clean_author, _clean_section
from src.store import merge_corpus
from src.timeutil import VN_TZ, parse_dt
from src.utils import canonicalize_url, content_hash, make_article_id


def test_canonicalize_url():
    assert canonicalize_url("HTTPS://VnExpress.net/a/b-123.html#top") \
        == "https://vnexpress.net/a/b-123.html"
    assert canonicalize_url("https://x.vn/p/?utm_source=fb&id=9") == "https://x.vn/p?id=9"
    assert canonicalize_url("https://x.vn/p/") == "https://x.vn/p"
    assert canonicalize_url("https://x.vn/") == "https://x.vn/"  # bare root keeps slash


def test_article_id_stable():
    u = "https://vnexpress.net/a-123.html"
    a, b = make_article_id(u), make_article_id(u)
    assert a == b and len(a) == 16
    assert make_article_id(u) != make_article_id("https://vnexpress.net/a-124.html")


def test_content_hash_whitespace_invariant():
    assert content_hash("xin  chào\n thế   giới") == content_hash("xin chào thế giới")
    assert content_hash(None) is None
    assert content_hash("   ") is None


def test_parse_dt_formats():
    # VnExpress RFC-822 with +0700 -> 11:43 local
    d = parse_dt("Tue, 23 Jun 2026 11:43:58 +0700")
    assert d is not None and str(d.tzinfo) == "Asia/Ho_Chi_Minh" and d.hour == 11
    # Tuoi Tre US-style, tz-naive -> assumed VN local, 10:58
    d = parse_dt("6/23/2026 10:58:00 AM")
    assert d is not None and d.hour == 10 and d.minute == 58 and d.tzinfo is not None
    # Nhan Dan RFC-822 with colon offset
    assert parse_dt("Tue, 23 Jun 2026 12:00:01 +07:00").hour == 12
    # ISO sitemap date
    assert parse_dt("2026-06-23T12:00:01+07:00").hour == 12
    # garbage
    assert parse_dt("not a date") is None and parse_dt(None) is None


def test_window_contains():
    cfg = load_config()
    now = datetime(2026, 6, 23, 12, 0, tzinfo=VN_TZ)
    w = resolve_window(cfg, now=now)
    assert w.contains(datetime(2026, 6, 20, 9, 0, tzinfo=VN_TZ))
    assert not w.contains(datetime(2026, 1, 1, tzinfo=VN_TZ))
    assert not w.contains(None)


def test_sniff_and_feed_parse():
    rss = (b'<?xml version="1.0"?><rss version="2.0"><channel>'
           b'<item><title>Hello</title>'
           b'<link>https://vnexpress.net/x-1.html</link>'
           b'<pubDate>Tue, 23 Jun 2026 11:43:58 +0700</pubDate>'
           b'<author>Nguyen Van A</author></item></channel></rss>')
    assert _sniff(rss) == "feed"
    outlet = {"slug": "vnexpress", "outlet_type": "semi_commercial"}
    recs = _parse_feed(rss, outlet, "thoi-su", "rss")
    assert len(recs) == 1
    r = recs[0]
    assert r.url == "https://vnexpress.net/x-1.html"
    assert r.section == "thoi-su" and r.author_hint == "Nguyen Van A"
    assert r.publish_hint is not None and r.publish_hint.hour == 11


def test_sniff_and_urlset_parse():
    sm = (b'<?xml version="1.0"?>'
          b'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
          b'xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">'
          b'<url><loc>https://nhandan.vn/a-post1.html</loc>'
          b'<news:news><news:publication_date>2026-06-23T12:00:01+07:00'
          b'</news:publication_date><news:title>T</news:title></news:news>'
          b'</url></urlset>')
    assert _sniff(sm) == "urlset"
    recs = _parse_urlset(sm, {"slug": "nhandan", "outlet_type": "party_official"})
    assert len(recs) == 1 and recs[0].url == "https://nhandan.vn/a-post1.html"
    assert recs[0].section is None and recs[0].publish_hint.hour == 12


def test_clean_author():
    assert _clean_author("TUOI TRE ONLINE; HỒNG QUANG⭐") == "HỒNG QUANG"
    assert _clean_author("Báo Nhân Dân điện tử; PHÚC THẮNG") == "PHÚC THẮNG"
    assert _clean_author("Nguyễn Thị Hà") == "Nguyễn Thị Hà"   # diacritics preserved
    assert _clean_author(None) is None and _clean_author("   ") is None


def test_cluster_near_dups():
    v = np.array([[1.0, 0.0], [1.0, 0.0], [0.0, 1.0], [0.92, 0.39]], dtype="float32")
    v = v / np.linalg.norm(v, axis=1, keepdims=True)
    labels = cluster_near_dups(v, threshold=0.82)
    assert labels[0] == labels[1] == labels[3]     # 0,1 identical; 3 cos≈0.92 merges
    assert labels[2] != labels[0]                  # orthogonal -> own cluster
    tight = cluster_near_dups(v, threshold=0.95)
    assert tight[0] == tight[1] and tight[3] != tight[0]   # only the exact pair merges


def test_cluster_near_dups_time_window():
    """The time constraint bounds chaining; it does not abolish it."""
    v = np.array([[1.0, 0.0]] * 3, dtype="float32")        # three identical vectors
    far = np.array([0, 3600, 100 * 3600], dtype="int64")   # 0h, 1h, 100h
    assert len(set(cluster_near_dups(v, 0.95))) == 1       # unconstrained -> one blob
    lab = cluster_near_dups(v, 0.95, timestamps=far, max_hours=24)
    assert lab[0] == lab[1] and lab[2] != lab[0]           # 100h-late row cannot link

    # Transitivity still applies *inside* the window: 0h-20h-40h chains via the
    # middle row even though the ends are 40h apart. This is why max_hours must
    # sit below the recurrence period of templated daily columns (24h), not above.
    near = np.array([0, 20 * 3600, 40 * 3600], dtype="int64")
    assert len(set(cluster_near_dups(v, 0.95, timestamps=near, max_hours=24))) == 1
    assert len(set(cluster_near_dups(v, 0.95, timestamps=near, max_hours=12))) == 3


def test_exact_dedupe():
    df = pd.DataFrame({
        "outlet": ["a", "b", "a"],
        "content_hash": ["h1", "h1", "h2"],
        "dedupe_cluster_id": [None, None, None],
    })
    out = assign_exact_duplicates(df)
    assert out["is_exact_duplicate"].tolist() == [False, True, False]
    stats = exact_duplicate_stats(out)
    assert stats["exact_duplicate_copies"] == 1
    assert stats["articles_with_body"] == 3
    assert abs(stats["exact_duplicate_rate"] - 1 / 3) < 1e-9


def test_first_category_html_entity():
    # entity ';' must be resolved before splitting, not truncate the label
    assert _first_category({"categories": "Th&#x1EBF; gi&#x1EDB;i"}) == "Thế giới"
    assert _first_category({"tags": ["Kinh t&#x1EBF;"]}) == "Kinh tế"
    assert _first_category({"categories": "A, B"}) == "A"     # real separator still splits
    assert _first_category({}) is None


def test_clean_section():
    assert _clean_section("thoi-su", "A headline") == "thoi-su"            # slug passes
    assert _clean_section("Th&#x1EBF", "x") == "Thế"                       # html-unescape
    assert _clean_section("Bắt ông X", "Bắt ông X") is None                # equals headline
    assert _clean_section("y" * 61, "h") is None                           # sentence-length
    assert _clean_section(None, "h") is None


def test_merge_corpus():
    existing = pd.DataFrame({
        "article_id": ["a", "b"],
        "scrape_datetime": ["2026-06-23T10:00", "2026-06-23T10:00"],
        "body": ["x", "y"],
    })
    new = pd.DataFrame({
        "article_id": ["b", "c"],
        "scrape_datetime": ["2026-06-24T10:00", "2026-06-24T10:00"],
        "body": ["y_new", "z"],
    })
    out = merge_corpus(existing, new)
    assert sorted(out["article_id"]) == ["a", "b", "c"]          # union, b deduped
    assert out.loc[out.article_id == "b", "body"].iloc[0] == "y_new"  # newest wins
    assert len(merge_corpus(None, new)) == 2                     # empty existing


def _run_all():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS {t.__name__}")
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print(f"FAIL {t.__name__}: {exc!r}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    return failed


if __name__ == "__main__":
    sys.exit(1 if _run_all() else 0)
