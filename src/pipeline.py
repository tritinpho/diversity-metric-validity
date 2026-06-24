"""End-to-end Phase-1 pipeline: discover -> fetch -> extract -> normalize ->
dedupe -> parquet -> data-quality report.

Run from the project root:

    python -m src.pipeline                 # full run + report
    python -m src.pipeline --max 100       # cap per outlet
    python -m src.pipeline --outlets vnexpress,tuoitre
    python -m src.pipeline --report-only   # rebuild report from existing parquet

Fetching is cached on disk, so a re-run only re-hits the network for URLs not
already cached (resumable). Outlets are processed round-robin so the per-domain
rate limit on one outlet overlaps with work on the others.
"""
from __future__ import annotations

import argparse
import logging

import pandas as pd

from src.collect.discover import discover_outlet
from src.collect.http import PoliteFetcher
from src.config import (
    Window,
    ensure_dirs,
    load_config,
    load_outlets,
    resolve_path,
    resolve_window,
    setup_logging,
)
from src.dedupe.hashing import assign_exact_duplicates
from src.extract.extract import extract_article
from src.normalize.schema import SCHEMA_COLUMNS, normalize_record
from src.report.quality import generate_report
from src.store import load_corpus, merge_corpus
from src.timeutil import now

_LOG = logging.getLogger("vnnews.pipeline")


def _select_outlets(reg: dict, only: str | None) -> list[dict]:
    outlets = reg["outlets"]
    if only:
        wanted = {s.strip() for s in only.split(",") if s.strip()}
        outlets = [o for o in outlets if o["slug"] in wanted]
    return outlets


def _process_one(record, fetcher: PoliteFetcher) -> dict:
    res = fetcher.fetch(record.url_raw, kind="html")
    extraction = extract_article(res.content, res.final_url or record.url_raw)
    return normalize_record(record, extraction, res)


def _collect(outlets: list[dict], fetcher: PoliteFetcher, window: Window, cfg: dict
             ) -> pd.DataFrame:
    # 1) Discover per outlet (RSS-first, sitemap backfill), already windowed+capped.
    discovered: dict[str, list] = {}
    for outlet in outlets:
        _LOG.info("discovering: %s (%s)", outlet["slug"], outlet["outlet_type"])
        discovered[outlet["slug"]] = discover_outlet(outlet, fetcher, window, cfg)

    total = sum(len(v) for v in discovered.values())
    _LOG.info("discovery complete: %d URLs across %d outlets", total, len(discovered))

    # 2) Round-robin fetch + extract + normalize.
    rows: list[dict] = []
    idx = {s: 0 for s in discovered}
    active = [s for s, v in discovered.items() if v]
    done = 0
    while active:
        for slug in list(active):
            i = idx[slug]
            queue = discovered[slug]
            if i >= len(queue):
                active.remove(slug)
                continue
            idx[slug] += 1
            rows.append(_process_one(queue[i], fetcher))
            done += 1
            if done % 25 == 0 or done == total:
                _LOG.info("processed %d/%d  (cache_hits=%d fetched=%d errors=%d)",
                          done, total, fetcher.stats["cache_hits"],
                          fetcher.stats["fetched"], fetcher.stats["errors"])

    df = pd.DataFrame(rows, columns=SCHEMA_COLUMNS)
    return df


def run(args: argparse.Namespace) -> None:
    cfg = load_config()
    setup_logging(cfg["logging"]["level"])
    ensure_dirs(cfg)
    if args.max is not None:
        cfg["collect"]["max_articles_per_outlet"] = args.max

    window = resolve_window(cfg)
    parquet_path = resolve_path(cfg, "articles_parquet")

    if args.report_only:
        if not parquet_path.exists():
            raise SystemExit(f"no corpus at {parquet_path}; run without --report-only")
        df = pd.read_parquet(parquet_path)
        _LOG.info("loaded %d rows from %s for reporting", len(df), parquet_path)
    else:
        reg = load_outlets()
        outlets = _select_outlets(reg, args.outlets)
        _LOG.info("window %s -> %s | outlets: %s | cap/outlet=%s | mode=%s",
                  window.start.date(), window.end.date(),
                  [o["slug"] for o in outlets],
                  cfg["collect"]["max_articles_per_outlet"],
                  "rebuild" if args.rebuild else "merge")

        fetcher = PoliteFetcher(cfg)
        new_df = _collect(outlets, fetcher, window, cfg)

        # Accumulate into the corpus (merge + dedupe by article_id) unless a
        # clean rebuild was requested. This is what fills the multi-week window
        # across daily runs instead of overwriting it each time.
        existing = None if args.rebuild else load_corpus(parquet_path)
        before = 0 if existing is None else len(existing)
        df = merge_corpus(existing, new_df)
        df = assign_exact_duplicates(df)
        # Near-duplicate (same-story) clustering is a separate on-demand pass:
        #   python -m src.dedupe.near_dup

        parquet_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(parquet_path, index=False)
        _LOG.info("corpus -> %s | collected=%d, added=%d, total=%d",
                  parquet_path, len(new_df), len(df) - before, len(df))
        _LOG.info("fetch stats: %s", fetcher.stats)

    if df.empty:
        _LOG.warning("corpus is empty; skipping report")
        return

    if not args.no_report:
        # Ensure dedupe columns exist when running --report-only on an older file.
        if "is_exact_duplicate" not in df.columns:
            df = assign_exact_duplicates(df)
        report_path = generate_report(df, cfg, window, generated_at=now())
        print(f"\nReport: {report_path}")

    _print_summary(df)


def _print_summary(df: pd.DataFrame) -> None:
    with_body = int(df["body"].notna().sum())
    print("\n================ RUN SUMMARY ================")
    print(f"articles:            {len(df)}")
    print(f"with extractable body: {with_body} "
          f"({100*with_body/len(df):.0f}%)" if len(df) else "")
    print("per outlet:")
    print(df.groupby(["outlet", "outlet_type"]).size().to_string())
    if "is_exact_duplicate" in df.columns:
        print(f"exact-duplicate copies: {int(df['is_exact_duplicate'].sum())}")
    print("=============================================")


def main() -> None:
    ap = argparse.ArgumentParser(description="VN news diversity — Phase 1 collector")
    ap.add_argument("--max", type=int, default=None,
                    help="cap articles per outlet (overrides config)")
    ap.add_argument("--outlets", type=str, default=None,
                    help="comma-separated outlet slugs to restrict to")
    ap.add_argument("--no-report", action="store_true", help="skip the report")
    ap.add_argument("--report-only", action="store_true",
                    help="rebuild the report from the existing parquet (no fetch)")
    ap.add_argument("--rebuild", action="store_true",
                    help="overwrite the corpus instead of merging into it")
    run(ap.parse_args())


if __name__ == "__main__":
    main()
