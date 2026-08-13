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


def test_build_texts_matches_production_construction():
    from src.dedupe.represent import build_texts

    h, b = ["Giá vàng hôm nay"], ["Sáng nay giá vàng tăng mạnh."]
    # Body window construction must stay byte-identical to the one in
    # near_dup.assign_near_duplicates, or recomputed baseline similarities stop
    # reproducing the stored calibration sample.
    assert build_texts(h, b, 600) == ["Giá vàng hôm nay. Sáng nay giá vàng tăng mạnh."]
    assert build_texts(h, b, 10) == ["Giá vàng hôm nay. Sáng nay g"]
    assert build_texts(h, b, 0) == ["Giá vàng hôm nay"]          # headline only
    assert build_texts([None], [None], 600) == ["."]             # nulls survive


def test_jaccard_shingle_similarity():
    from src.dedupe.represent import SPECS, _sim_jaccard

    spec = dict(SPECS["jaccard_syl5_body3000"])
    spec["shingle"] = 2
    texts = ["a b c d", "a b c d", "x y z w"]
    pairs = np.array([[0, 1], [0, 2]])
    sim = _sim_jaccard(spec, texts, pairs)
    assert sim[0] == 1.0            # identical shingle sets
    assert sim[1] == 0.0            # disjoint
    # Documents shorter than the shingle length have no shingles at all; the
    # union is then empty and the score must be 0, not a ZeroDivisionError.
    assert _sim_jaccard(spec, ["a", "a"], np.array([[0, 1]]))[0] == 0.0


def test_pair_similarity_row_subsetting_is_invariant():
    """Restricting to the rows a pair touches must not change the score."""
    from src.dedupe.represent import _sim_jaccard, SPECS

    spec = dict(SPECS["jaccard_syl5_body3000"])
    spec["shingle"] = 2
    full = ["p q r s", "zz yy", "p q r s", "aa bb cc"]
    # Same two documents, once at indices 0/2 of a longer list and once alone.
    assert (_sim_jaccard(spec, full, np.array([[0, 2]]))[0]
            == _sim_jaccard(spec, [full[0], full[2]], np.array([[0, 1]]))[0])


def test_calibration_weights_are_horvitz_thompson():
    from src.dedupe.calibrate import _weights

    lab = pd.DataFrame({"band_lo": [0.7, 0.7, 0.9], "band_hi": [0.8, 0.8, 1.0],
                        "label": [1, 0, 1]})
    strata = [{"band_lo": 0.7, "band_hi": 0.8, "population": 1000},
              {"band_lo": 0.9, "band_hi": 1.0, "population": 50}]
    w = _weights(lab, strata)
    assert list(w) == [500.0, 500.0, 50.0]        # population / labels in band
    # A band that was sampled but never labelled must be dropped, not counted as
    # containing zero true pairs — that would inflate precision silently.
    w2 = _weights(lab, strata + [{"band_lo": 0.5, "band_hi": 0.6, "population": 9}])
    assert list(w2) == [500.0, 500.0, 50.0]


def test_weighted_precision_recall_curve():
    from src.dedupe.calibrate import _curve

    sim = np.array([0.9, 0.8, 0.7])
    y = np.array([1, 0, 1])
    w = np.array([10.0, 10.0, 100.0])
    c = _curve(sim, y, w).set_index("threshold")
    # At 0.9: retrieves 10 weighted pairs, all true, of 110 true overall.
    assert c.loc[0.9, "precision"] == 1.0
    assert round(c.loc[0.9, "recall_in_pool"], 4) == round(10 / 110, 4)
    # At 0.7 everything is retrieved: recall 1, precision 110/120.
    assert c.loc[0.7, "recall_in_pool"] == 1.0
    assert round(c.loc[0.7, "precision"], 4) == round(110 / 120, 4)


def _toy_sparse_pool(n=120, seed=3):
    """A small normalized sparse matrix plus sorted timestamps, for scan tests."""
    from scipy import sparse

    rng = np.random.default_rng(seed)
    d = np.abs(rng.normal(size=(n, 24)))
    d[d < 1.0] = 0.0
    d[:, 0] = 0.4                      # a term every document shares
    X = sparse.csr_matrix(d / np.linalg.norm(d, axis=1, keepdims=True)).astype("float32")
    secs = np.sort(rng.integers(0, 3 * 86400, size=n)).astype("int64")
    return X, secs


def test_sparse_scan_histogram_is_exact_and_windowed():
    """Band populations are Horvitz-Thompson denominators, so they must be counts."""
    from src.dedupe.calibrate import (SCAN_BINS, band_populations, sparse_pair_scan)

    X, secs = _toy_sparse_pool()
    bands = [(0.10, 0.30, 3), (0.30, 1.01, 3)]
    full = (X @ X.T).toarray()
    ref = np.array([full[i, j] for i in range(len(secs))
                    for j in range(i + 1, len(secs))
                    if secs[j] - secs[i] <= 12 * 3600])

    hist, _, _, _ = sparse_pair_scan(X, secs, 12.0, bands, block=16)
    assert hist.sum() == len(ref)                    # j > i triangle, 12h window
    assert np.array_equal(
        hist, np.bincount(np.clip((ref * SCAN_BINS).astype("int32"), 0, SCAN_BINS),
                          minlength=SCAN_BINS + 1))
    pops = band_populations(hist, bands)
    for lo, hi, _ in bands:
        assert pops[(lo, hi)] == int(((ref >= lo) & (ref < hi)).sum())


def test_sparse_scan_sample_is_block_size_invariant():
    """The draw keys off pair identity, not arrival order, so it must not move."""
    from src.dedupe.calibrate import sparse_pair_scan

    X, secs = _toy_sparse_pool()
    bands = [(0.10, 0.30, 3), (0.30, 1.01, 3)]
    key = lambda I, J: sorted(zip(I.tolist(), J.tolist()))  # noqa: E731
    _, I1, J1, _ = sparse_pair_scan(X, secs, 12.0, bands, seed=5, block=16, capacity=6)
    _, I2, J2, _ = sparse_pair_scan(X, secs, 12.0, bands, seed=5, block=97, capacity=6)
    assert key(I1, J1) == key(I2, J2)
    # ...and a different seed must give a different sample, or it is not random.
    _, I3, J3, _ = sparse_pair_scan(X, secs, 12.0, bands, seed=6, block=16, capacity=6)
    assert key(I1, J1) != key(I3, J3)


def test_sparse_scan_excludes_pairs_without_shrinking_the_population():
    """Earlier rounds leave the band population alone — only the sample shrinks."""
    from src.dedupe.calibrate import sparse_pair_scan

    X, secs = _toy_sparse_pool()
    bands = [(0.10, 1.01, 8)]
    h0, I0, J0, _ = sparse_pair_scan(X, secs, 12.0, bands, seed=5, capacity=8)
    drop = (I0[:3].astype("uint64") * np.uint64(len(secs)) + J0[:3].astype("uint64"))
    h1, I1, J1, _ = sparse_pair_scan(X, secs, 12.0, bands, exclude_keys=drop,
                                     seed=5, capacity=8)
    assert np.array_equal(h0, h1)
    got = set((I1.astype("uint64") * np.uint64(len(secs)) + J1.astype("uint64")).tolist())
    assert not got & set(drop.tolist())


def test_band_populations_reject_off_grid_edges():
    """An edge inside a histogram bin would make the population an interpolation."""
    from src.dedupe.calibrate import SCAN_BINS, band_populations

    hist = np.ones(SCAN_BINS + 1, dtype="int64")
    assert band_populations(hist, [(0.10, 0.125, 1)])[(0.10, 0.125)] == 5
    try:
        band_populations(hist, [(0.101, 0.125, 1)])
    except ValueError:
        return
    raise AssertionError("off-grid band edge was silently accepted")


def test_strata_and_labels_never_pool_across_designs(tmp_path=None):
    """Band edges mean different things on different similarity scales."""
    import json
    from pathlib import Path
    from tempfile import mkdtemp

    from src.dedupe.calibrate import LEGACY_DESIGN, _merge_strata

    d = Path(tmp_path or mkdtemp())
    # Legacy file carries no representation field and must read as the baseline.
    (d / "strata.json").write_text(json.dumps(
        [{"band_lo": 0.7, "band_hi": 0.8, "population": 100, "sampled": 5}]))
    (d / "strata_r3.json").write_text(json.dumps(
        [{"band_lo": 0.7, "band_hi": 0.8, "population": 999, "sampled": 5,
          "representation": "tfidf_syl12_hl_body1200"}]))
    assert _merge_strata(d, LEGACY_DESIGN)[0]["population"] == 100
    assert _merge_strata(d, "tfidf_syl12_hl_body1200")[0]["population"] == 999
    # The two share a band key while describing different scales, so an
    # unqualified merge must refuse rather than pick one.
    try:
        _merge_strata(d)
    except SystemExit:
        return
    raise AssertionError("strata from two designs were pooled")


def test_operating_point_is_lowest_threshold_meeting_precision():
    """Pre-registered rule: buy recall subject to a precision floor."""
    from src.dedupe.calibrate import operating_point

    tbl = pd.DataFrame({"threshold": [0.1, 0.2, 0.3, 0.4],
                        "precision": [0.50, 0.91, 0.88, 0.97],
                        "recall_in_pool": [1.0, 0.7, 0.5, 0.2]})
    # 0.2 qualifies and 0.4 qualifies; the rule takes the lower, keeping recall.
    # It must not stop at the first dip back below the floor (0.3) either.
    assert operating_point(tbl, 0.90)["threshold"] == 0.2
    assert operating_point(tbl, 0.95)["threshold"] == 0.4
    assert operating_point(tbl, 0.99) is None       # unreachable floor, not a crash


def test_retired_strata_are_dropped_from_the_pool():
    import json
    from pathlib import Path
    from tempfile import mkdtemp

    from src.dedupe.calibrate import _merge_strata

    d = Path(mkdtemp())
    (d / "strata.json").write_text(json.dumps(
        [{"band_lo": 0.9, "band_hi": 1.0, "population": 10, "sampled": 5}]))
    (d / "strata_r2.json").write_text(json.dumps(
        [{"band_lo": 0.5, "band_hi": 0.6, "population": 999, "sampled": 5,
          "retired": True}]))
    bands = _merge_strata(d)
    assert [(b["band_lo"], b["band_hi"]) for b in bands] == [(0.9, 1.0)]


def test_agreement_on_binary_labels():
    from src.dedupe.calibrate import agreement

    ids = [f"p{i}" for i in range(10)]
    a = pd.DataFrame({"pair_id": ids, "label": [1] * 5 + [0] * 5})
    assert agreement(a, a.copy())["observed_agreement"] == 1.0
    assert agreement(a, a.copy())["cohen_kappa"] == 1.0

    b = a.copy()
    b.loc[0, "label"] = 0                       # one disagreement in ten
    st = agreement(a, b)
    assert st["n"] == 10 and st["disagreements"] == 1
    assert round(st["observed_agreement"], 3) == 0.9
    # Hand-computed from the coincidence matrix: with 10 pairs there are N=20
    # values, o_01 = o_10 = 1, marginals n_0 = 11 and n_1 = 9, so
    # D_o = 2/20 = 0.1 and D_e = 2*11*9/(20*19) = 0.5210, giving 0.8081.
    # Kappa uses each coder's own marginal instead and gives 0.80 — the two are
    # close but not equal, and neither should silently become the other.
    assert round(st["krippendorff_alpha"], 4) == 0.8081
    assert round(st["cohen_kappa"], 4) == 0.8000
    # Skipped pairs come back from the sheet as "" and must be dropped, not
    # counted as agreement — the export writes '' for a deliberate skip.
    c = a.astype({"label": object})
    c.loc[9, "label"] = ""
    assert agreement(a, c)["n"] == 9


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
