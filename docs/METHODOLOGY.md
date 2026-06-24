# Methodology

> **Status:** working draft for the researcher to refine. Inline `[DECIDE: …]`
> markers flag genuine method choices that need a human decision. Formulas are
> given for the working draft; final notation/normalisation should be confirmed
> against the cited sources in [RELATED_WORK.md](RELATED_WORK.md).

This is the operational core. It specifies, for every metric, **what it
captures, its formula, required inputs, parameters, and how it is computed on the
snapshot**, then specifies the **validity analyses** that constitute the study's
contribution.

It builds on the corpus produced by Phase 1 and the schema described in the
[README](../README.md) (one row per article: `article_id`, `outlet`,
`outlet_type`, `section`, `publish_datetime`, `body`, `word_count`,
`content_hash`, `dedupe_cluster_id`, and the near-duplicate columns added by the
deduplication pass). It does not restate the schema or the phase plan; see the
[README](../README.md) and [RESEARCH_DESIGN.md](RESEARCH_DESIGN.md).

**Notation.** A *category distribution* `p = (p_1, …, p_S)` is a set of
non-negative shares summing to 1 over `S` categories (categories may be topics,
sections, or outlets depending on the metric). `N` is the number of articles in
the unit being summarised.

---

## 0. Preprocessing inputs the metrics depend on

The metrics below consume four derived layers. Each is a measurement decision in
its own right, so each is parameterised and later varied in
[§5 Validity analyses](#5-validity-analyses).

1. **Word segmentation.** Vietnamese words span multiple syllables, so whitespace
   is not a token boundary; bodies are segmented before any token-based step.
   `word_count` already uses this (underthesea in Phase 1).
   `[DECIDE: segmenter for the analysis layer — underthesea vs. pyvi vs.
   VnCoreNLP. Phase 1 used underthesea; fixing one (with version pin) and noting
   the alternative as a sensitivity check is enough.]`
2. **Topic / issue assignment.** A topic layer is required for every content- and
   agenda-diversity metric. Options below in [§2](#2-content--topic-diversity).
   `[DECIDE: topic method — (a) unsupervised model induced from this corpus
   (LDA / NMF / BERTopic or contextualized topic models over multilingual or
   PhoBERT/Vietnamese-adapted embeddings), (b) a classifier onto an imposed
   taxonomy (e.g. IPTC Media Topics), (c) an LLM-based / prompt-based scheme
   (e.g. TopicGPT), or (d) an induced AND an imposed layer, so the
   imposed-vs-induced contrast becomes the topic-taxonomy validity test in §5.2.
   Any LLM-based layer must be validated task-by-task against human labels (see
   RELATED_WORK cluster (b), recent/SOTA). Recommendation: induced + imposed (d),
   with any LLM layer as a separately-validated optional arm.]`
3. **Near-duplicate / same-story clusters.** Already computed
   (`near_dup_cluster_id`) via multilingual sentence embeddings + connected
   components at a calibrated cosine threshold (0.94). Used directly by the
   syndication metrics and by the deduplicated unit of analysis.
4. **Section harmonisation.** Raw `section` is not portable across outlets
   (controlled slugs vs. editorial categories vs. article-level tags vs. none —
   documented in the [Phase-1 report](../reports/quality_report.md)). Any
   section-based metric requires a harmonised layer first.
   `[DECIDE: harmonise raw sections into a common scheme, or abandon raw
   `section` for metrics and rely solely on the induced/imposed topic layer? The
   report shows raw sections are not comparable; recommendation is to treat the
   non-portability as a *finding* (§5.2) and use the topic layer for metrics.]`

**Unit of analysis.** Every distributional metric is computed at two units, and
the pair is compared in [§5.1](#51-syndication-inflation):

- **Article unit** — one row = one article.
- **Story unit** — one row = one near-duplicate cluster (syndicated copies
  collapsed to a single story; canonical row per cluster).

`[DECIDE: for the story unit, how to pick the canonical row (first-published?
longest body? originating outlet if identifiable?) and how to attribute a
collapsed story's outlet/section. Affects source-diversity counts directly.]`

---

## 1. Source / outlet diversity

**Captures:** how concentrated vs. spread the supply is across sources — i.e.
whether a few outlets/sources account for most of the published cross-section.

Let outlets (or sources — see the unit decision) be indexed `i = 1…S` with
article shares `p_i = n_i / N`.

### 1.1 Distinct source count and effective number of sources

- Raw distinct count: `S` (number of outlets/sources present).
- Effective number of sources (Hill number of order 1):
  $$ {}^{1}\!D = \exp\!\Big(-\sum_{i=1}^{S} p_i \ln p_i\Big) $$
  the number of equally-frequent sources that would give the same entropy — more
  interpretable than raw `S` when shares are skewed.

### 1.2 Concentration: HHI and concentration ratio

- Herfindahl–Hirschman Index:
  $$ \mathrm{HHI} = \sum_{i=1}^{S} p_i^2 \in [1/S,\ 1] $$
  higher = more concentrated. Note `HHI = 1 / {}^{2}\!D`, the inverse of the
  order-2 Hill number, linking it to the diversity family in §2.
- Concentration ratio `CR_k = Σ_{i=1..k} p_(i)` (top-`k` outlets' share of
  output). `[DECIDE: k for CR_k — k=4 is conventional from media-economics; state
  and justify.]`

### 1.3 Gini of outlet output

Gini coefficient over the `n_i` (inequality of output volume across outlets):
$$ G = \frac{\sum_{i}\sum_{j} |n_i - n_j|}{2 S \sum_i n_i} \in [0,1] $$

**Required inputs:** `outlet` (and/or the chosen source unit), article counts;
optionally `near_dup_cluster_id` for the story unit.
**Parameters:** source unit (outlet / author / wire agency); article vs. story
unit; `k` for `CR_k`.
**Computed on the snapshot:** tabulate `n_i` per source over the window, derive
shares, compute all of the above at both units. Report alongside `outlet_type`
as a covariate (group-wise concentration), never as an outlet ranking with
evaluative language.

> **Supply-side note / adaptation.** "Source diversity" in the Western
> literature often presumes outlets are *independent* competing sources. Heavy
> syndication violates this: the same wire copy inflates apparent source counts.
> The **redundancy-adjusted** source count (computed at the story unit, §1.1 on
> collapsed clusters) is the supply-side correction; the gap between
> article-unit and story-unit source diversity is the inflation quantified in
> [§5.1](#51-syndication-inflation).
> `[DECIDE: define "source" for the headline number — registered outlet, or
> originating producer (wire agency) where detectable. The two answer different
> questions; report both if feasible.]`

---

## 2. Content / topic diversity

**Captures:** how varied the *content* of the supply is, over a category
distribution `p` of topics (per outlet, per type, or pooled).

Requires the **topic layer** from [§0](#0-preprocessing-inputs-the-metrics-depend-on).
All three classic indices below are monotone functions of the same `p`; computing
all three is deliberate — their agreement is the convergent-validity check in
[§5.4](#54-convergent-validity).

### 2.1 Shannon entropy (and evenness)

$$ H(p) = -\sum_{i=1}^{S} p_i \ln p_i , \qquad J = \frac{H(p)}{\ln S}\in[0,1] $$
`H` rises with both richness (`S`) and evenness; Pielou's `J` isolates evenness.

### 2.2 Simpson / Gini–Simpson

$$ \lambda = \sum_{i=1}^{S} p_i^2 \quad(\text{dominance}), \qquad
   \text{Gini–Simpson} = 1 - \lambda $$
probability that two randomly drawn articles fall in *different* topics.

### 2.3 Gini coefficient over topic shares

Same formula as §1.3 applied to topic counts — inequality of attention across
topics (one dominant topic ⇒ high Gini).

### 2.4 Hill numbers (unifying frame)

$$ {}^{q}\!D = \Big(\sum_{i} p_i^{q}\Big)^{1/(1-q)} $$
"effective number of topics" of order `q`: `q=0` → richness `S`; `q→1` →
`exp(H)`; `q=2` → `1/λ`. Reporting the **Hill profile** over `q ∈ [0,2]` makes
entropy/Simpson differences visible on one interpretable (counts) scale.

### 2.5 Disparity-aware diversity (Stirling variety/balance/disparity)

Classic indices treat topics as equidistant. Stirling's framework adds
**disparity** `d_ij` (how *different* topics `i` and `j` are):
$$ \Delta = \sum_{i \ne j} d_{ij}\, p_i\, p_j $$
with `d_ij` from distances between topic centroids in embedding space.
`[DECIDE: include disparity-aware diversity? It is the most defensible "content
diversity" notion but adds an embedding-distance step and parameters (which
embedding, how to define topic centroids). Recommendation: include as a
secondary metric — it directly tests whether "more topics" also means "more
*different* topics," a likely break point under homogeneous supply.]`

**Required inputs:** per-article topic labels or topic-probability vectors;
`outlet`/`outlet_type` for grouping; embeddings if computing disparity.
**Parameters:** topic method and `K`; segmenter; grouping level (outlet / type /
pooled); article vs. story unit; `q` grid for Hill; embedding for disparity.
**Computed on the snapshot:** build `p` at each grouping level, compute
§2.1–§2.5; report per outlet, per `outlet_type`, and pooled.

> **Supply-side note.** These indices are natively supply-side (they describe a
> published distribution), so no exposure re-specification is needed — but their
> *validity* hinges entirely on the topic layer, which is exactly what
> [§5.2](#52-topic-taxonomy-validity) interrogates.

---

## 3. Cross-outlet agenda overlap / divergence

**Captures:** how similar or distinct outlets' agendas are — do outlets cover the
same topic mix (overlap) or different ones (divergence)?

Let `p^{(a)}` be outlet `a`'s topic distribution and
`m = \frac{1}{S}\sum_a p^{(a)}` (or a size-weighted) pooled "system agenda."

### 3.1 Pairwise Jensen–Shannon divergence

$$ \mathrm{JSD}(p\,\|\,q) = \tfrac12 D_{\mathrm{KL}}(p\,\|\,M) + \tfrac12 D_{\mathrm{KL}}(q\,\|\,M),\quad M=\tfrac12(p+q) $$
symmetric, bounded in `[0, ln 2]` (or `[0,1]` in bits / with base-2 log).
Produces an `S×S` outlet-divergence matrix; `1 − JSD`-style similarity feeds an
overlap heatmap and optional hierarchical clustering of outlets.
`[DECIDE: cluster outlets from the JSD matrix and compare the recovered grouping
to `outlet_type`? A clean recovery is evidence the metric detects real
structure; report as descriptive, not evaluative.]`

### 3.2 RADio-style calibration (supply-side adaptation)

In its native (recommender) form, **calibration** measures the divergence between
the topic distribution of a user's *recommendations* and that user's *reading
history*. There is no user or reading history here.

**Supply-side re-specification:** calibration of outlet `a` = divergence between
the outlet's published agenda and a **reference distribution**:
$$ \mathrm{Cal}(a) = \mathrm{JSD}\big(p^{(a)} \,\|\, r\big) $$
where `r` is the pooled system agenda `m` (how far each outlet departs from the
system-wide mix) — or a within-type reference (how far it departs from its
structural peers).
`[DECIDE: reference distribution r for supply-side calibration — pooled system
agenda, within-`outlet_type` agenda, or an external reference (e.g. a Western
corpus's topic mix). Each answers a different question; pooled is the minimal,
self-contained choice.]`
`[DECIDE: RADio uses rank-aware divergences (positions weighted by attention) for
ranked recommendation lists. The published cross-section is a *set*, not a ranked
list, so the rank-aware weighting is dropped unless a supply-side salience proxy
(e.g. homepage position, recency, section prominence) is introduced. Default:
drop rank-awareness and state it; note the proxy as an extension.]`

### 3.3 RADio-style fragmentation (supply-side adaptation)

Native **fragmentation** measures how much users' recommendation *sets* overlap
(a fragmented public sphere = little common ground). Re-specified to supply:
fragmentation = the extent to which outlets cover **disjoint vs. shared stories**,
computed from the **same-story clusters** (§4) rather than topics:
$$ \mathrm{Frag} = 1 - \frac{\#\{\text{stories covered by} \ge 2\ \text{outlets}\}}{\#\{\text{stories}\}} $$
(or a pairwise story-set Jaccard averaged over outlet pairs). High fragmentation
= outlets share few stories; low = heavy common coverage / syndication.
`[DECIDE: define fragmentation over same-story clusters (story-level overlap) or
over topic distributions (agenda-level overlap)? They measure different things;
the story-level version is the more direct supply-side analogue and reuses the
dedup clusters. Report both, label clearly.]`

### 3.4 RADio metrics that require exposure/stance data — out of scope or deferred

RADio's remaining normative metrics assume data this study does not have, and are
**flagged rather than forced**:

- **Activation** (emotional/mobilising intensity) and **Representation**
  (distribution of stances/actors) require sentiment/stance annotation.
- **Alternative Voices** (minority/marginal viewpoint presence) requires actor or
  viewpoint coding.
- **Calibration to a user** and any *exposure-weighted* form require interaction
  data.

`[DECIDE: attempt a stance/actor layer (e.g. named-entity / actor extraction) to
approximate Representation, or declare Activation/Representation/Alternative
Voices out of scope for this snapshot and list them as future work?
Recommendation: out of scope for Phase 3–4; they need annotation infrastructure
that is a project of its own and risks the neutrality framing.]`

**Required inputs:** per-outlet topic distributions (§2) for 3.1–3.2;
`near_dup_cluster_id` + `outlet` for 3.3.
**Parameters:** log base / normalisation for JSD; reference `r`; weighting
(uniform vs. size-weighted); story- vs. topic-level fragmentation.
**Computed on the snapshot:** build per-outlet `p^{(a)}`, the JSD matrix,
calibration per outlet against `r`, and fragmentation from the cluster table.

---

## 4. Syndication / redundancy

**Captures:** how much of the supply is *the same story repeated* — the
redundancy that most directly threatens source-diversity validity here.

From the deduplication layer (`content_hash` for exact; `near_dup_cluster_id` for
near-duplicate/same-story):

- **Exact-duplicate rate** = verbatim copies / articles with body.
- **Near-duplicate (same-story) rate** = near-dup copies / articles with body.
- **Cross-outlet same-story clusters** = clusters spanning ≥2 outlets, and the
  number of articles within them (the syndication/overlap signal).
- **Redundancy-adjusted effective sources** = §1.1 recomputed on the story unit.
- **Per-outlet syndication share** = fraction of an outlet's articles that belong
  to a cross-outlet cluster (how much of each outlet's output is shared copy).

*Phase-1 reference values* (provisional, on the accumulating snapshot): exact-dup
rate ≈ 0.5%; near-dup same-story copies ≈ 3.4%; **44 cross-outlet same-story
clusters (92 articles)** vs. only **3 (6 articles)** from exact hashing — i.e.
embedding near-dup surfaces ~15× more cross-outlet overlap than exact matching.
See the [Phase-1 report](../reports/quality_report.md).

**Required inputs:** `content_hash`, `near_dup_cluster_id`, `outlet`.
**Parameters:** the near-dup cosine **threshold** (calibrated 0.94 — see
[§5.3](#53-parameter-sensitivity)); embedding model; `embed_body_chars` (chars of
headline+body embedded).
**Computed on the snapshot:** tabulate the rates above overall, per outlet, and
per `outlet_type`.

> **Supply-side note.** This family is the lever for the central validity claim:
> syndication is a structural feature of this ecosystem that classic
> source-diversity metrics do not model, so the redundancy measures both
> *quantify* it and *feed the correction* applied in §1 and tested in §5.1.

---

## 5. Validity analyses

These analyses — not the metric values themselves — are the study's
contribution. Each targets a research question in
[RESEARCH_DESIGN.md](RESEARCH_DESIGN.md#2-research-questions).

### 5.1 Syndication inflation

_Targets RQ2 (and RQ1)._ Recompute every distributional metric (§1–§3) at the **article unit** and the
**story unit** (syndicated copies collapsed). Report the **inflation** =
article-unit minus story-unit value, per metric, overall and per `outlet_type`.
*Claim under test:* classic source-diversity metrics overstate diversity in
proportion to syndication; the story unit is the needed re-specification.
`[DECIDE: headline inflation statistic — absolute difference, ratio, or rank
change in the outlet ordering? Rank change is the most communicative.]`

### 5.2 Topic-taxonomy validity

_Targets RQ2._ Test whether a **Western-derived imposed taxonomy** fits Vietnamese news as well
as an **induced** topic layer:

- Fit (a) an imposed-taxonomy classifier and (b) an induced model; compare
  **topic coherence** (e.g. NPMI / `c_v`), the share of articles in a
  catch-all/"other" topic, and human face-validity of top terms.
- Quantify **section non-portability** directly: show the raw `section`
  vocabulary is incommensurable across outlet types (controlled slugs vs.
  editorial categories vs. tags vs. none), motivating the harmonised/induced
  layer. (The [Phase-1 report](../reports/quality_report.md) already exhibits
  this.)
`[DECIDE: which imposed taxonomy to test (IPTC Media Topics is the journalism
standard; an alternative is a Western news-topic-model label set). Pick one and
justify; this is the crux of "are Western taxonomies valid here".]`
`[DECIDE: whether a small human-coded validation set (face validity of topic
assignments) is feasible — even ~200 articles dual-coded would let you report a
reliability figure and pre-empt the "no gold standard" critique (cf. RELATED_WORK
cluster (b)).]`
`[DECIDE: include an LLM-based topic/issue-assignment arm as a SOTA comparator?
2023–2026 work shows LLM annotation can match human coders but requires
task-specific validation against human labels and prompt-stability checks (see
RELATED_WORK cluster (b), recent/SOTA). If included, treat it as a separately
validated arm, not the primary topic layer.]`

### 5.3 Parameter sensitivity

_Targets RQ3._ Vary, one at a time and jointly, the analyst degrees of freedom and report how
much each metric and the **outlet ranking** move:

- **Topic count `K`** (grid, e.g. 10–100).
- **Embedding / topic model** — vary the representation backbone (the current
  multilingual MiniLM vs. SOTA multilingual embedders such as multilingual-E5,
  BGE-M3, or gte-multilingual, vs. a Vietnamese-adapted encoder such as
  PhoBERT / CafeBERT) and the topic model (LDA vs. NMF vs. BERTopic); use a
  benchmark (MTEB / MMTEB; VN-MTEB for Vietnamese) to justify the choice — see
  RELATED_WORK cluster (d), recent/SOTA.
  `[DECIDE: keep the lightweight MiniLM as the primary dedup/embedding backbone
  (fast, reproducible, and model choice is covered here as a sensitivity arm), or
  upgrade the primary to a SOTA multilingual embedder? If upgrading, re-calibrate
  the near-dup threshold — the 0.94 cosine cutoff is model-specific and does not
  transfer across encoders.]`
- **Near-dup threshold** (sweep around the calibrated 0.94; the Phase-1 note
  shows < 0.92 over-merges same-*topic* articles into cross-outlet blobs while
  ≥ 0.94 isolates same-*story* — i.e. the metric is threshold-sensitive in a
  documentable way).
- **Segmenter** (underthesea vs. alternative).

Report stability as rank correlation (Spearman) of outlet orderings across
settings and coefficient of variation of each index.
`[DECIDE: define a primary "stability" pass/fail criterion in advance (e.g.
"outlet rank correlation ≥ 0.8 across the K grid"), ideally pre-registered, so
sensitivity results are not read post hoc.]`

### 5.4 Convergent validity

_Targets RQ4; covers both convergent and discriminant validity._

- **Convergent:** metrics that should agree should correlate — Shannon `H`,
  Gini–Simpson, and Hill `^1D`/`^2D` across outlets; HHI vs. Gini of output.
  Report the correlation matrix; near-perfect correlation among the topic indices
  is the *expected* convergent result and a sanity check on the pipeline.
- **Discriminant:** metrics that capture *different* facets (e.g. topic diversity
  vs. source concentration; cf. Voakes et al.) should **not** be redundant —
  report their (lower) correlation as evidence each adds information.

### 5.5 Random / shuffled baselines

_Targets RQ4 (and RQ1)._ Establish that the metrics detect **structure**, not corpus artefacts:

- **Label-shuffle null:** permute outlet (or topic) labels across articles, keep
  marginal sizes, recompute cross-outlet JSD / fragmentation / calibration; build
  a null distribution over many permutations; the observed value's percentile is
  a permutation `p`-value for "outlets differ more than chance."
- **Random-assignment null:** assign articles to topics at random (matching the
  topic marginal) and recompute content-diversity indices to show the observed
  values are not what random sparsity would yield.
- **Size/sparsity controls:** subsample outlets to equal `N` to confirm
  differences are not driven by unequal article counts.
`[DECIDE: number of permutations and the multiple-comparison correction for the
pairwise-outlet tests (e.g. 1,000+ permutations; Holm/BH across pairs).]`

---

## 6. Reproducibility and reporting

- Every metric is computed from the canonical corpus + a fixed config; all
  parameters (`K`, threshold, model, unit) are recorded with each result so a run
  is reproducible from `outlets.yaml` + `config.yaml` + the window.
- All results are reported in **neutral measurement language** (concentration,
  overlap, redundancy, divergence), conditioned on `outlet_type` as a covariate,
  with **no** evaluative ranking of outlets and no claims about editorial intent.
- Numerical outputs, the parameter grids of §5.3, and the baseline distributions
  of §5.5 are released with the code (see
  [DATA_MANAGEMENT_AND_ETHICS.md](DATA_MANAGEMENT_AND_ETHICS.md)).

`[DECIDE: pre-register §5.3–§5.5 (parameters, stability thresholds, permutation
counts) on OSF before computing final metrics? Strongly recommended to protect
the validity claim from researcher-degrees-of-freedom criticism.]`
