# Research Design

> **Status:** working draft for the researcher to refine. Inline `[DECIDE: …]`
> markers flag genuine research-design choices that need a human decision before
> they are locked. Nothing here is final until those are resolved.

This document states the purpose, research questions, contribution, scope, and
target venue for the study, and explains how it fits the measurement-validity
agenda in computational communication science. It assumes the framing and scope
in the repository [README](../README.md) ("Framing & scope") and the corpus
schema and roadmap described there; it does not restate them.

> **A note on framing sources.** The neutral, supply-side framing that governs
> this project is carried in the public [README](../README.md). These `docs/`
> files are intended to become the canonical, citable statement of design and
> method for the preprint and dataset release.
> `[DECIDE: confirm that README + docs/ are the single public source of truth for
> framing and schema, so the project does not depend on any repo-excluded notes.]`

---

## 1. Purpose

News-diversity metrics — measures of how varied the news on offer is, across
sources, topics, and viewpoints — were developed and validated almost entirely
on **Western, high-choice, English-language** media markets. Their numerical
behaviour, interpretability, and the constructs they assume (distinct competing
sources, portable topic categories, broadly independent outlets) are calibrated
to that setting.

Vietnam's online-news ecosystem is **structurally different**: state-aligned
ownership across much of the field, heavy wire-service syndication (a single
agency's copy reappearing across many outlets), and a distinct outlet ecology
(party organs, mass-organisation dailies, semi-commercial generalists,
lifestyle/entertainment portals, sector outlets). That structural difference
makes it a **natural stress test** for the metrics.

The study therefore asks a **measurement-validity** question, not a substantive
one. The question is **not** "is Vietnamese news diverse?" It is: *do
established news-diversity metrics remain interpretable and stable when the media
structure they assume no longer holds — and, where they break, what
re-specification do they need?*

This is **supply-side** measurement throughout: we characterise the diversity of
what outlets *publish* (the published cross-section). We do not measure exposure,
what users see, or recommender effects. See [scope](#4-scope) below.

---

## 2. Research questions

All four are phrased as questions about the **measures**, not about the media
system. Each maps to one or more validity analyses in
[METHODOLOGY.md](METHODOLOGY.md#5-validity-analyses).

**RQ1 — Interpretability and stability.**
Do established diversity metrics (source/outlet concentration; topic diversity
via Shannon entropy, Gini, Simpson/Hill numbers; cross-outlet divergence via
Jensen–Shannon; calibration- and fragmentation-style measures) yield
**interpretable, non-degenerate values** on a Vietnamese supply-side snapshot —
or do they saturate, floor, or collapse to uninformative ranges?

**RQ2 — Construct validity of the inputs.**
Are the constructs these metrics presuppose actually valid in this ecosystem?
Specifically: (a) is "a source" well-defined when the same wire copy is
republished across outlets; (b) is "a topic/section" a portable construct when
outlets expose incompatible section vocabularies (controlled slugs vs.
editorial categories vs. article-level tags vs. none — already observed in the
[Phase-1 report](../reports/quality_report.md)); (c) are outlets statistically
**independent units** when syndication links them?

**RQ3 — Robustness to analyst degrees of freedom.**
How sensitive are the metric values and the resulting outlet rankings to choices
the analyst must make: number of topics *K*, topic-model/embedding-model choice,
the near-duplicate similarity threshold, the unit of analysis (article vs.
deduplicated story), and whether syndicated duplicates are collapsed?

**RQ4 — Convergent validity and signal detection.**
Do metrics that *should* agree actually agree (e.g. entropy, Simpson, and Hill
numbers as monotone re-expressions of the same distribution; concentration vs.
Gini)? And do the metrics detect **real structure** — i.e. do observed values
depart from what shuffled/random baselines produce, confirming the measures
capture signal rather than artefacts of corpus size or sparsity?

`[DECIDE: keep four RQs, or split a fifth explicit "what minimal re-specification
restores interpretability?" RQ out of the Contribution? Recommendation: keep
re-specification in the Contribution so the RQs stay diagnostic and the payoff
stays one thing.]`

`[DECIDE: should any RQ make an explicit cross-system comparison (compute the
same metrics on a Western reference corpus and compare metric *behaviour*), or
is the validity argument purely internal (sensitivity + convergent + baseline)?
A Western anchor strengthens external/construct-validity claims but roughly
doubles the data and preprocessing burden and invites scope creep. See §3.]`

---

## 3. Contribution

The contribution is the **validity finding plus reusable measurement
infrastructure** — explicitly *not* "the first Vietnamese news dataset."

1. **A measurement-validity assessment** of each metric family on a media system
   they were not designed for: where each stays interpretable, where it breaks,
   and *why* (which structural feature — syndication, taxonomy heterogeneity,
   ownership homogeneity — breaks which assumption).
2. **Re-specification recommendations**: concrete, minimal adjustments that
   restore interpretability (e.g. redundancy-adjusted source counts that collapse
   same-story clusters; an induced rather than imposed topic layer; a
   supply-side reinterpretation of calibration/fragmentation against a pooled
   reference). Each recommendation is tied to the assumption it repairs.
3. **Reusable Vietnamese measurement infrastructure**: a documented, RSS-first
   snapshot corpus (schema in the [README](../README.md)), a reproducible
   preprocessing + metrics pipeline, and a [datasheet](DATASHEET.md) — released
   under a rehydration-only model (see
   [DATA_MANAGEMENT_AND_ETHICS.md](DATA_MANAGEMENT_AND_ETHICS.md)).

`[DECIDE: how strongly to foreground the corpus as a standalone artefact. It has
independent value, but the brief is firm that the validity finding is the
headline. Recommendation: corpus = enabling infrastructure, validity = headline.]`

---

## 4. Scope

**In scope (supply-side, snapshot):**

- The **published cross-section**: articles published by the outlet set over a
  fixed snapshot window, with full text + metadata per the corpus schema.
- **Outlet structural type** (`outlet_type`) as a neutral covariate for
  conditioning the analysis.
- Metrics over **what is published**: source/outlet concentration, topic/content
  diversity, cross-outlet agenda overlap/divergence, and
  syndication/redundancy from deduplication clusters.

**Out of scope (and why):**

- **Exposure and audience.** We do not measure what users see, click, or are
  recommended. Those require interaction/exposure data we do not have, and they
  are a different validity question. Metrics with a native *exposure* or *user*
  definition (e.g. recommender-diversity measures defined relative to a user
  profile or reading history) are either re-specified to a supply-side reference
  or marked out of scope in [METHODOLOGY.md](METHODOLOGY.md). 
- **Editorial intent, control, or influence.** The study makes no claims about
  why coverage looks as it does. Findings are stated in measurement terms
  (concentration, overlap, redundancy), never as claims about any outlet's
  motives or about the ecosystem.
- **Causal or longitudinal claims.** A snapshot supports cross-sectional
  description and metric-validity testing, not trends or causes.
  `[DECIDE: snapshot only, or collect a second non-adjacent window later to test
  temporal stability of the metrics? A second window is the single cheapest
  robustness add, but is not required for Phase-1 validity claims.]`

**Scoping choices to lock:**

- **DECIDED 2026-07-13, REVISED 2026-07-22:** snapshot window fixed at
  **2026-06-24 → 2026-07-22** (29 days). Dense day-to-day collection actually
  began 2026-06-24 (the first full-volume day; 2026-06-19 → 2026-06-23 has only
  a handful of stray backfilled articles from deep sitemap sweeps and should be
  treated as pre-window noise, not part of the reported snapshot). Originally
  fixed at 2026-07-21 (28 days / 4 calendar weeks); extended by one day when
  the Jul 21 noon collection run was found to have silently failed entirely
  (scheduled-task phantom-skip) and had to be recovered via a Jul 22 manual
  catch-up — rather than close the window on a day that only existed via
  next-day recovery, the cutoff moved to Jul 22, the day collection actually
  ran to completion. Collection ran on the existing daily/topup cadence through
  2026-07-22, then stopped for good: the `news-diversity-daily-collect`
  scheduled task was permanently disabled the same day after a persistent
  phantom-skip failure pattern, and no further manual topups follow. Report
  that contiguous range as *the* snapshot regardless of what `config.yaml`'s
  rolling `days_back` has accumulated beyond it.
- `[DECIDE: final outlet set. 16 outlets across all 5 structural types are
  collected; Lao Động is deferred (bot-gated, needs a JS renderer) and Baomoi is
  excluded as an aggregator. Confirm the released set and whether to invest in
  recovering Lao Động for balance within the union/mass-daily type.]`
- `[DECIDE: how aggregators enter the design. Exclude Baomoi entirely, or include
  it in a *separate* analysis as a syndication/redundancy probe (it is, in
  effect, a ground-truth republisher)? Excluding keeps the corpus "original
  publishers only"; including gives a useful upper bound on overlap.]`
- `[DECIDE: unit of analysis for "source diversity" — outlet, byline/author, or
  originating wire agency. Author is missing for some outlet types (e.g. ~99%
  null at one outlet, per the Phase-1 report), and wire attribution is often
  implicit; the choice materially changes every source-diversity number. See
  RQ2(a).]`

---

## 5. Target venue

The work is positioned for a **methodological / measurement** venue.

- **Computational Communication Research (CCR)** — open-access, explicitly
  methods- and computation-friendly, and receptive to measurement-validity and
  tooling contributions. Best fit for the headline (validity of computational
  measures) and for releasing reusable infrastructure.
- **Digital Journalism** — higher-profile in journalism studies and the natural
  home for news-diversity / news-flows substance; aligns with the target
  supervisor's area, but is less oriented to a purely computational
  measurement-validity argument.

`[DECIDE: primary venue. Recommendation: CCR as primary (the contribution is
measurement validity + open infrastructure, and OA suits a PhD-application
artefact), with Digital Journalism as the alternative if the framing is pushed
toward news-flows substance. Confirm against the supervisor's preference.]`

`[DECIDE: preprint + open-science posture. arXiv (cs.CL / cs.CY) plus an OSF
project; whether to pre-register the analysis plan (especially the sensitivity
and baseline tests) before computing final metrics, to pre-empt
researcher-degrees-of-freedom criticism. Recommendation: a lightweight OSF
pre-analysis note for RQ3/RQ4 strengthens the validity claim at low cost.]`

---

## 6. Fit with the computational-communication-science measurement-validity agenda

Computational communication science has repeatedly argued that automated
measures must be **validated**, not assumed: that text-as-data methods import
constructs and parameters whose validity is setting-dependent, and that
cross-lingual / cross-system transfer is where those constructs are most likely
to fail silently. (Anchor literature is mapped in
[RELATED_WORK.md](RELATED_WORK.md), clusters (b) and (c).)

This project is a concrete instance of that agenda:

- It treats diversity metrics as **measurement instruments** and subjects them to
  standard validity checks — interpretability, construct validity, robustness to
  analyst choices, convergent validity, and discrimination from a null baseline.
- It targets the **transfer** case the agenda flags as highest-risk: instruments
  calibrated on one media system, applied to a structurally different,
  non-English one.
- It contributes **reusable, documented infrastructure** (corpus + pipeline +
  datasheet) so the validity claims are reproducible and extendable — itself a
  methodological norm the field promotes.

The operational detail — exact metrics, formulas, inputs, parameters, and the
validity analyses — is in [METHODOLOGY.md](METHODOLOGY.md). The literature map is
in [RELATED_WORK.md](RELATED_WORK.md). Data handling, ethics, and release are in
[DATA_MANAGEMENT_AND_ETHICS.md](DATA_MANAGEMENT_AND_ETHICS.md).
