# Datasheet

Following **Gebru et al. (2021), "Datasheets for Datasets"**
(https://doi.org/10.1145/3458723). This is the datasheet for the eventual public
release of the Vietnamese news supply-side snapshot.

> **Status:** template, pre-filled where known and marked **TODO** otherwise.
> Numbers labelled *(provisional)* come from the accumulating Phase-1 corpus (see
> the [Phase-1 report](../reports/quality_report.md)) and will be replaced with
> the finalised snapshot's values at release. The release is **rehydration-only**
> (URLs + hashes + derived features, not article bodies) — see
> [DATA_MANAGEMENT_AND_ETHICS.md](DATA_MANAGEMENT_AND_ETHICS.md). Resolve open
> `[DECIDE: …]` items in the linked docs before finalising.

---

## Motivation

**For what purpose was the dataset created?**
To enable a **measurement-validity** study: testing whether established
news-diversity metrics remain interpretable and stable when applied to the
Vietnamese online-news ecosystem, a media system they were not developed for. The
dataset is the supply-side snapshot those metrics are computed on (see
[RESEARCH_DESIGN.md](RESEARCH_DESIGN.md)). It is deliberately positioned as
**reusable measurement infrastructure**, not as "the first Vietnamese news
dataset."

**Who created the dataset and on whose behalf?**
The researcher (PhD applicant); contact `<PROJECT_CONTACT>`. TODO: institutional
affiliation if any.

**Who funded the creation of the dataset?**
TODO (self-funded / grant / none).

---

## Composition

**What do the instances represent?**
Online news **articles** (one row per article) from Vietnamese news outlets,
each with text + metadata per the schema in the [README](../README.md).

**How many instances are there in total?**
*(Provisional)* ≈ **1,706 articles across 16 outlets**, all 5 structural
`outlet_type` categories, accumulating toward the snapshot window. **TODO:**
final counts at release.

**Does the dataset contain all possible instances or a sample?**
A **sample**: a snapshot of recently-published articles discovered via each
outlet's RSS feeds and sitemaps over the collection window, capped per outlet per
run. It is **not** a census of the outlets' output and is biased toward what
"latest" feeds/sitemaps expose at collection time. `[DECIDE: per-outlet cap and
window — see RESEARCH_DESIGN scope decisions.]`

**What data does each instance consist of?**
Both raw-ish and derived features: `article_id`, `outlet`, `outlet_type`, `url`,
`url_raw`, `headline`, `body` (working corpus only; **not redistributed**),
`section`, `publish_datetime`, `scrape_datetime`, `author`, `word_count`, `lang`,
`content_hash`, `dedupe_cluster_id`, near-duplicate cluster fields, and provenance
(`discovery_source`, `seg_method`, `fetch_status`). Topic assignments and metric
outputs are added in Phases 2–3.

**Is there a label or target associated with each instance?**
No supervised target. The analysis uses `outlet_type` as a covariate and derived
**topic** assignments; `section` is present but **not portable across outlets**
(a measurement finding, not a clean label) — see the [Phase-1
report](../reports/quality_report.md) and
[METHODOLOGY.md](METHODOLOGY.md#52-topic-taxonomy-validity).

**Is any information missing from individual instances?**
Yes, and missingness correlates with outlet type *(provisional, from the Phase-1
report)*: overall ≈ 0.6% missing body, ≈ 3.0% missing section, 0% missing publish
datetime, ≈ 13.1% missing author (concentrated in specific outlets, e.g. ~99%
author-null at one outlet, ~16% at another; some outlets expose no reliable
per-section feed so `section` is null/page-derived). This asymmetry is itself an
object of the validity analysis.

**Are relationships between instances made explicit?**
Yes — **near-duplicate / same-story clusters** (`dedupe_cluster_id`,
`near_dup_cluster_id`) link articles that are the same story, including across
outlets (the syndication signal). *(Provisional: 44 cross-outlet same-story
clusters / 92 articles.)*

**Are there recommended data splits?**
Not applicable (no train/test task); the corpus is analysed as a cross-section.

**Are there errors, sources of noise, or redundancies?**
Yes: extraction noise from `trafilatura` on some layouts; noisy/page-derived
`section` values (tags, event names); intentional redundancy (syndicated copies)
retained and flagged rather than removed. Exact-duplicate rate *(provisional)*
≈ 0.5%.

**Is the dataset self-contained or does it rely on external resources?**
At release it **relies on external resources by design**: article bodies are
**not** included and must be **rehydrated** from the source URLs (rehydration-only
model). Risk of link rot over time; content hashes are shipped for verification.
See [DATA_MANAGEMENT_AND_ETHICS.md](DATA_MANAGEMENT_AND_ETHICS.md#4-release-model-rehydration-only).

**Does the dataset contain confidential / sensitive data?**
No confidential data. The only personal data is the **published author byline**
(already public). No private individuals are profiled; no user data. `[DECIDE:
author handling in the release — include / hash / omit.]` Content may mention
public individuals as news subjects (incidental, unprocessed).

**Does the dataset identify sub-populations / is it offensive?**
`outlet_type` records each outlet's neutral structural category; it is a
covariate, not an evaluation. No demographic sub-population coding. News text may
contain sensitive topics as published; no additional annotation is added.

---

## Collection process

**How was the data associated with each instance acquired?**
Directly observable: fetched from outlets' public RSS feeds, sitemaps, and
article pages. Metadata (URL, section, publish date) comes from feeds/sitemaps
where available; body/author/date are extracted from article HTML via
`trafilatura` (with cleaning/normalisation). Discovery preference: RSS → sitemap
→ listing.

**What mechanisms or procedures were used to collect the data?**
A Python pipeline (`src/`): polite cached HTTP (rate-limited, jittered,
backoff, robots-respecting, descriptive identifiable User-Agent), trafilatura
extraction, schema normalisation (timezone → `Asia/Ho_Chi_Minh`, language
detection, Vietnamese word segmentation), exact-hash dedup inline, and embedding
near-duplicate clustering as a separate pass. Validated by `precheck` and offline
smoke tests.

**If a sample, what was the sampling strategy?**
Convenience/temporal: whatever the per-outlet feeds and sitemaps surfaced during
the window, capped per outlet per run; the corpus accumulates over daily runs.
Not probabilistic.

**Over what timeframe was the data collected?**
*(Provisional)* collection window 2026-06-03 → 2026-06-24 (project timezone),
dense on the most recent days. **TODO:** final contiguous window at release.

**Were any ethical review processes conducted?**
TODO: state whether institutional ethics/IRB review applies (typically minimal
for public-text supply-side collection, but confirm). Ethics posture documented
in [DATA_MANAGEMENT_AND_ETHICS.md](DATA_MANAGEMENT_AND_ETHICS.md).

**Does the dataset relate to people?**
Only via public author bylines and incidental mentions of public figures in news
text; no data collected from or about data subjects directly, no notification/
consent mechanism applicable to public news content. `[DECIDE: takedown/correction
policy — see ethics plan §9.]`

---

## Preprocessing / cleaning / labeling

**Was any preprocessing/cleaning/labeling done?**
Yes: URL canonicalisation + stable `article_id` hashing; HTML→main-text
extraction; boilerplate removal; headline/author cleaning (strip outlet-name
tokens, decorative symbols); timezone normalisation; language detection;
Vietnamese **word segmentation** before token counts (underthesea in Phase 1);
exact-content hashing; embedding-based near-duplicate clustering (multilingual
sentence encoder, cosine threshold **0.94**, calibrated — see
[METHODOLOGY.md](METHODOLOGY.md#53-parameter-sensitivity)). Topic assignment and
section harmonisation are Phase-2 steps. **TODO:** finalise topic layer.

**Was the raw data saved in addition to the preprocessed data?**
Yes — raw HTML/RSS are cached locally (`data/raw/`, gitignored) but **not
released** (rehydration model). `[DECIDE: restricted/dark archive of raw HTML for
verification-on-request?]`

**Is the preprocessing software available?**
Yes — all code is released (see Distribution). A run is reproducible from
`outlets.yaml` + `config.yaml` + the window.

---

## Uses

**What (other) tasks could the dataset be used for?**
Supply-side news-diversity measurement; cross-outlet agenda/overlap analysis;
syndication/redundancy studies; Vietnamese-language NLP benchmarking (topic
modeling, near-duplicate detection); comparative media-systems work; and as a
testbed for measurement-validity of text-derived metrics.

**Is there anything about the composition or collection that might affect future
uses?**
Yes — users **must** account for: (a) the temporal/feed-driven sampling (not a
census); (b) syndication/redundancy (treat outlets as non-independent); (c)
non-portable `section`; (d) author-missingness by outlet type; (e) the
supply-side scope (no exposure claims). These are documented to **prevent**
inappropriate use (e.g. ranking outlets, inferring editorial intent, or making
exposure/audience claims).

**Are there tasks for which the dataset should not be used?**
It should **not** be used to make claims about audience exposure, editorial
intent, censorship, or political control; nor to evaluate or rank outlets
normatively. The framing is neutral and measurement-focused (see
[README](../README.md)).

---

## Distribution

**How will the dataset be distributed?**
As a public, versioned, rehydration-only release (derived features + URLs +
hashes + rehydration script + code + this datasheet). `[DECIDE: host + DOI —
Zenodo assumed.]`

**When will it be distributed?**
At preprint submission (Phase 5). TODO: date.

**Licence / IP / ToS.**
Code under an OSI licence; derived data under a permissive data licence; **article
text is not redistributed** (rights remain with outlets/authors). `[DECIDE: MIT
vs Apache-2.0 for code; CC BY 4.0 vs CC0 for derived data — see ethics plan §6.]`

**Have any third parties imposed IP-based or other restrictions?**
Outlet copyright/ToS apply to article text (hence rehydration-only). Third-party
tools/models retain their own licences. TODO: enumerate at release.

**Do any export controls or regulatory restrictions apply?**
TODO: confirm none.

---

## Maintenance

**Who will be supporting/hosting/maintaining the dataset?**
The researcher; contact `<PROJECT_CONTACT>`. TODO: long-term steward.

**How can the owner/curator be contacted?**
`<PROJECT_CONTACT>`.

**Is there an erratum?**
TODO: maintain an errata/changelog with the release.

**Will the dataset be updated?**
`[DECIDE: snapshot-only (one DOI, no updates) vs. periodic re-snapshots (new DOI
per version). A snapshot study argues for the former; reusable infrastructure
argues for the latter.]` Versioning: one DOI per snapshot version.

**If it relates to people, are there applicable retention limits?**
Author bylines are public; `[DECIDE: retention/deletion plan for the working
corpus with bodies — see ethics plan §7.]`

**Will older versions continue to be supported?**
TODO.

**If others want to extend/build on the dataset, is there a mechanism?**
Yes — open code + rehydration script + this datasheet enable re-collection and
extension; contributions/issues via the public repository. TODO: contribution
guidance.
