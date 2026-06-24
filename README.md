# Vietnamese News Diversity — corpus & measurement-validity study

A research project building (a) a structured **snapshot** corpus of Vietnamese
online news across multiple outlets, and (b) a **measurement-validity** analysis
testing whether news-diversity metrics developed for Western media behave
sensibly — or need re-specification — when applied to the Vietnamese news
ecosystem.

This is **supply-side** measurement: we characterise the diversity of what
outlets *publish* (the published cross-section). We do not measure exposure or
what users see. Outlet `outlet_type` is neutral structural metadata used as a
covariate.

## Framing & scope

This is a **methodological / measurement** study — not a critique of any outlet
or of the ecosystem. The contribution is a test of *measurement validity*:
whether news-diversity metrics developed for Western media yield interpretable,
stable values when applied to this ecosystem, and where their assumptions need
re-specification.

- **Supply-side only.** We measure the diversity of the published cross-section —
  what outlets *publish*. We do **not** measure exposure, what users see, or
  recommender effects; that would require interaction data we do not have.
- **Neutral measurement language.** Results are described in measurement terms —
  *concentration of coverage*, *topic overlap across outlets*, *supply
  diversity* — not as claims about editorial intent or control.
- **Outlet type is a covariate.** `outlet_type` records each outlet's structural
  category as neutral metadata used to condition the analysis; it is not an
  evaluation of any outlet.

Output: a preprint, a documented public dataset (with a datasheet), and
reproducible code.

## Roadmap

1. **Corpus** *(current)* — a clean, deduplicated snapshot across the outlet set
   over a 2–4 week window, with full article text and metadata.
2. **Preprocessing** — Vietnamese word segmentation, topic/issue assignment, and
   near-duplicate clustering (the same story across outlets).
3. **Metrics** — established diversity metrics (source/outlet; topic/content via
   entropy, Gini, Simpson) plus supply-side adaptations, computed on the
   cross-section.
4. **Validity analysis** *(the core contribution)* — test each metric for
   interpretable, stable values; identify where assumptions break and what
   re-specification is needed.
5. **Release** — preprint, repository, and dataset with a datasheet.

> **Status:** Phase 1 complete — 16 outlets spanning all 5 structural types in
> `outlets.yaml`, collected into an accumulating corpus (all robots-compliance
> checked). Phase 2 starting: embedding-based near-duplicate (same-story)
> clustering. (Lao Động deferred — bot-gated; Baomoi excluded as an aggregator.)

## Pipeline

```
discover (RSS → sitemap → listing)  →  fetch (polite, cached)  →
extract (trafilatura)  →  normalize (schema, tz, lang, VN segmentation)  →
dedupe (exact content-hash inline; embedding near-dup as a separate pass)  →
data/processed/articles.parquet  →  data-quality report
```

Discovery is **RSS-first** (clean URL + section + publish date), falling back to
sitemaps, and only then to listing-page scraping. Fetching respects
`robots.txt`, rate-limits per domain with jitter, sends a descriptive
User-Agent, caches every response, and backs off on transient errors.

**Building the window over time.** RSS "latest" feeds only return the most
recent items (≈ the last day or two), so one run is a single-day cross-section.
To reach the 2–4 week target the corpus *accumulates*: feeds/sitemaps are
re-polled every run (article HTML stays cached), and each run's rows are merged
into `articles.parquet` and de-duped by `article_id` (newest scrape wins). Run
daily and the window fills; pass `--rebuild` to start the corpus fresh.

## Reproduce from scratch

```powershell
# 1. Environment (Python 3.11+)
python -m venv .venv
.\.venv\Scripts\Activate.ps1            # Windows PowerShell
# source .venv/bin/activate             # macOS/Linux
pip install -r requirements.txt

# 2. (optional) run the offline unit tests
python tests\test_smoke.py

# 3. Collect + report. Merges into the corpus by default (run daily to
#    accumulate the window); caps per outlet for a trial pass.
python -m src.pipeline --max 100

# Other entry points
python -m src.pipeline --rebuild                     # overwrite corpus (fresh start)
python -m src.pipeline --outlets vnexpress,tuoitre   # subset
python -m src.pipeline --report-only                 # rebuild report from parquet
python -m src.collect.precheck                       # robots/discovery compliance check
python -m src.dedupe.near_dup                         # near-dup (same-story) clustering
```

Outputs:

| Path | What |
| --- | --- |
| `data/raw/` | cached RSS/sitemaps + article HTML (gitignored, re-fetchable) |
| `data/processed/articles.parquet` | the canonical corpus (one row per article) |
| `reports/quality_report.md` + `reports/figures/` | data-quality report + plots |

## Configuration

- **`config.yaml`** — collection window, per-domain rate limits, retry/backoff,
  paths, the per-outlet cap. Nothing outlet-specific.
- **`outlets.yaml`** — outlet slugs, `outlet_type` (controlled vocab), and the
  RSS/sitemap URLs per outlet. All discovery sources live here.

A run is reproducible from `outlets.yaml` + `config.yaml` + the date window.

## Schema (one row per article)

`article_id`, `outlet`, `outlet_type`, `url`, `url_raw`, `headline`, `body`,
`section`, `publish_datetime` (ISO-8601, `Asia/Ho_Chi_Minh`), `scrape_datetime`,
`author`, `word_count` (segmented Vietnamese tokens), `lang`, `content_hash`,
`dedupe_cluster_id`, plus provenance columns (`discovery_source`, `seg_method`,
`fetch_status`).

## Repo layout

```
src/collect/    RSS/sitemap discovery + polite cached fetch
src/extract/    trafilatura wrapper (+ per-site override hook)
src/normalize/  schema mapping, tz, language detect, VN segmentation
src/dedupe/     exact content-hash now; embedding near-dup (Phase 2)
src/report/     data-quality report
src/pipeline.py orchestrator / CLI
tests/          offline smoke tests
```

## Notes on the starter outlets

- **VnExpress** (`semi_commercial`) and **Tuổi Trẻ** (`union_mass_daily`) expose
  rich per-section RSS; Tuổi Trẻ additionally provides `<author>` in RSS.
- **Nhân Dân** (`party_official`) returns the same "home" feed for any `/rss/*`
  path and uses flat article URLs, so per-section metadata is largely
  unavailable; it is discovered via its Google-News sitemap and its `section` is
  recorded as null. This metadata asymmetry across outlet types is itself an
  observation for the Phase-4 validity analysis, not a defect.
