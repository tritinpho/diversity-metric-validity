# Data Management & Ethics Plan

> **Status:** working draft for the researcher to refine. Inline `[DECIDE: …]`
> markers flag choices that need a human decision. **This document is not legal
> advice.** Copyright, data-protection, and computer-access law differ by
> jurisdiction and change over time; confirm anything legally consequential with
> a qualified adviser and your institution before release.

Throughout, a contact is written as **`<PROJECT_CONTACT>`** — a placeholder for a
**non-personal** address (a dedicated project inbox or an institutional address),
never a personal email.
`[DECIDE: set <PROJECT_CONTACT> to a non-personal address and use it in the
crawler User-Agent, the dataset record, and the preprint. Note: the current
config.yaml User-Agent embeds a personal email; replace it before any further
collection or release.]`

---

## 1. What is collected

- **Unit:** one record per online news article, per the corpus schema in the
  [README](../README.md) (URL, headline, body text, section, publish/scrape
  datetimes, author-as-published, outlet + `outlet_type`, language, word count,
  content hash, dedup cluster ids, and provenance columns).
- **Sources:** publicly accessible articles from the outlet set in
  `outlets.yaml`, discovered RSS-first (then sitemap, then listing), over a
  fixed snapshot window.
- **Not collected:** no user/audience data, no behavioural or interaction data,
  no login-gated or paywalled content, no comments threads, no private
  messages, no personal data beyond the **published author byline**. The study
  is supply-side only (see [RESEARCH_DESIGN.md](RESEARCH_DESIGN.md#4-scope)).
- **Scale:** a bounded snapshot (~16 outlets; Phase-1 corpus ≈ 1,700 articles
  and accumulating toward the window). Not a continuous or open-ended crawl.

---

## 2. Legal considerations (not legal advice)

- **Copyright in article text.** News articles are typically protected by
  copyright held by the outlet or author. Vietnam is a Berne Convention member;
  most jurisdictions of likely readership (EU, US) also protect such text.
  Collecting copies for **private research/analysis** is generally lower-risk
  than **redistributing** full text. This is the central reason the dataset is
  released **rehydration-only** (§4): we do not republish article bodies.
- **Research/“fair” exceptions vary.** Text-and-data-mining and
  research/quotation exceptions exist in some jurisdictions (e.g. EU TDM
  provisions, fair use/fair dealing elsewhere) but are uneven and fact-specific;
  do not assume they authorise redistribution.
  `[DECIDE: identify the governing jurisdiction(s) for the release (researcher's
  institution + repository host, e.g. Zenodo/CERN) and confirm the redistribution
  posture with the institution. Document the basis in the datasheet.]`
- **Terms of service.** Some outlets' ToS restrict automated access or reuse.
  Where collection relies on the generic `robots.txt` allowance (see §3),
  document that, and keep collection within the polite limits below.
- **Database/extraction rights** may attach to feeds/sitemaps in some
  jurisdictions; releasing only URLs + hashes + derived features (not the
  underlying database) mitigates this.

> The project's posture: **minimise legal exposure by construction** — collect
> for analysis, cache locally, and release only non-infringing derivatives.

---

## 3. robots.txt and polite-crawling conduct

The collector is built to be a polite, identifiable citizen, and this conduct is
itself part of the dataset's credibility and reproducibility:

- **Respect `robots.txt`.** `respect_robots: true`; the parser checks each URL
  before fetching, and the robots file is cached per domain.
- **Rate-limit per domain** with jitter (default ≥ 2.5 s + up to 1 s jitter
  between requests to the same host), honour any declared `Crawl-delay`, and back
  off exponentially on transient errors.
- **Identify the crawler** with a descriptive User-Agent that includes
  `<PROJECT_CONTACT>`, so outlets can contact the project.
- **Cache everything** (raw RSS/sitemaps + article HTML) so re-runs do not re-hit
  servers; collection is resumable and idempotent (merge by `article_id`).
- **Pre-flight check.** `python -m src.collect.precheck` confirms robots
  permission and discovery liveness per outlet before a run.

> **A conduct question to resolve explicitly.** Several outlets' `robots.txt`
> *disallow named* research/AI crawlers (e.g. specific bot tokens) while
> *allowing* a generic `User-agent: *`. The project's User-Agent is a descriptive,
> contactable token that matches the generic `*` allowance rather than any named
> disallow. This is technically permitted by the sites' own rules, but a
> reviewer may ask whether matching `*` respects the *spirit* of those
> directives.
> `[DECIDE: how to handle this. Options: (a) keep the generic-matching,
> fully-identified UA and document the reasoning transparently (permitted by the
> stated rules; identifiable; rate-limited; non-commercial research; no full-text
> redistribution); (b) additionally honour the strictest interpretation by
> excluding any outlet whose robots.txt signals intent to bar research crawlers;
> (c) seek explicit permission from affected outlets. Recommendation: at minimum
> (a) — document it plainly in the datasheet and preprint so the choice is
> defensible and auditable; consider (c) for any outlet where it matters.]`

---

## 4. Release model: rehydration-only

To respect copyright while keeping the work reproducible, the public dataset is
**rehydration-only**: it ships the *recipe and derivatives*, not the article
bodies.

**Released:**
- Per-article **canonical URL** + **`article_id`** + **`content_hash`** (so others
  can re-fetch and verify they obtained the same text).
- **Derived, non-infringing features**: `outlet`, `outlet_type`, `section`
  (raw + harmonised), `publish_datetime`, `word_count`, `lang`, dedup/near-dup
  cluster ids, topic assignments, and the computed metric outputs.
- A **rehydration script** that re-fetches bodies from the URLs under the same
  polite policy, plus a manifest with hashes for integrity.
- All **code**, configs (`outlets.yaml`, `config.yaml` with `<PROJECT_CONTACT>`),
  and the [datasheet](DATASHEET.md).

**Not released:** raw article **body text**, raw cached HTML.

`[DECIDE: release short, non-substitutive derivatives that aid reproducibility
without republishing the work — e.g. headline only, or only the leading N tokens
/ a bag-of-words or embedding vector per article? Embeddings/word-frequency
vectors are common in TDM releases and are far less substitutive than full text,
but the line is jurisdiction-dependent. Default: release headlines + derived
features + embeddings; withhold bodies.]`
`[DECIDE: repository + DOI host (Zenodo is the working assumption) and dataset
versioning (one DOI per snapshot version).]`

> **Reproducibility caveat (state it plainly):** rehydration degrades over time
> as URLs change or articles are removed (“link rot”). Mitigations: ship content
> hashes for verification; record `scrape_datetime`; report the expected
> rehydration success rate; `[DECIDE: whether to deposit raw HTML in a
> restricted/dark archive for verification-on-request without public
> redistribution.]`

---

## 5. Personal-data minimisation (author handling)

The only personal data collected is the **published author byline** (already
public, attached to the article). Even so, minimise:

- Store the author **as published**; never enrich, cross-link, or profile
  authors. No attempt to identify private individuals.
- The byline is cleaned to the person name(s) (outlet-name tokens and decorative
  symbols stripped) — incidental, not enrichment.
- For people who appear **as subjects** in article text, no special processing,
  extraction, or profiling is performed (no actor/entity database is built;
  see the out-of-scope RADio metrics in [METHODOLOGY.md](METHODOLOGY.md#3-cross-outlet-agenda-overlap--divergence)).

`[DECIDE: author field in the public release — (a) include author-as-published
(it is already public and supports byline-level source analysis), (b) pseudonymise
(hash) author names, or (c) omit author from the release. Data-protection regimes
(e.g. GDPR for EU readers, Vietnam's PDPD) treat names as personal data; weigh
research value against minimisation. Recommendation: decide jointly with the
unit-of-analysis choice in METHODOLOGY §1 — if byline-level source diversity is
not a headline metric, omit or hash author in the release.]`

---

## 6. Licensing

- **Code:** an OSI-approved open-source licence.
  `[DECIDE: MIT vs. Apache-2.0. Apache-2.0 adds an explicit patent grant and is
  common for research tooling; MIT is simplest. Recommendation: MIT unless the
  institution prefers Apache-2.0.]`
- **Derived data (features, metrics, cluster ids, harmonised labels):** a
  permissive data licence.
  `[DECIDE: CC BY 4.0 (attribution) vs. CC0 (public domain dedication). CC BY
  eases citation tracking for a PhD artefact; CC0 maximises reuse.
  Recommendation: CC BY 4.0 for the derived data.]`
- **Article text:** **not licensed for redistribution** by this project — rights
  remain with the original outlets/authors; only URLs + hashes are shared so users
  re-obtain text from the source. State this explicitly in the datasheet.
- **Third-party components** (models, toolkits) retain their own licences; record
  them (e.g. the embedding model, segmenters — see
  [RELATED_WORK.md](RELATED_WORK.md) cluster (d)).

---

## 7. Storage and handling

- **Raw cache** (`data/raw/`: HTML, feeds, robots) is **local and gitignored** —
  re-fetchable, never committed, never published.
- **Processed corpus** (`data/processed/articles.parquet`) is the canonical
  working artefact; it contains body text and so is **not** committed/published as
  full text (release follows §4).
- **Backups / retention:** `[DECIDE: where the working corpus (with bodies) is
  stored and backed up during the project, who has access, and the
  retention/deletion plan after publication. A private institutional store with a
  stated retention period is the conventional answer.]`
- **Integrity:** runs are deterministic and resumable; `content_hash` enables
  verification; `scrape_datetime` records provenance.

---

## 8. Pre-publication check (run before any push or release)

A blocking checklist before the repo, dataset, or preprint goes public:

- [ ] **No personal contact details** in code, configs, docs, commit metadata, or
  the dataset — all contacts are `<PROJECT_CONTACT>`. *(Note: replace the personal
  email currently in `config.yaml`'s User-Agent.)*
- [ ] **No credentials, tokens, API keys, or internal paths** in tracked files.
- [ ] **No full article body text or raw HTML** in the public dataset (rehydration
  model only, §4).
- [ ] **Author field** handled per the §5 decision (include / hash / omit).
- [ ] **Framing/neutrality review:** all public text uses neutral measurement
  language; `outlet_type` is described as a covariate; no claims about editorial
  intent, control, or political characterisation of any outlet (see
  [README](../README.md) "Framing & scope").
- [ ] **Licences present**: code licence + data licence files; third-party
  licences acknowledged; full-text-not-redistributed notice in the datasheet.
- [ ] **Datasheet complete**: no remaining `TODO` in released-version
  [DATASHEET.md](DATASHEET.md).
- [ ] **Reproducibility**: README "reproduce from scratch" works from a clean
  checkout; rehydration script runs and reports success rate.
- [ ] **robots/polite-crawling conduct** documented, including the `*`-matching
  decision (§3).

`[DECIDE: make this checklist a CI/pre-commit gate (e.g. a secrets/PII scan +
a check that bodies are absent from any released artefact) rather than a manual
list?]`

---

## 9. Contact & governance

- **Contact:** `<PROJECT_CONTACT>` for questions, corrections, or takedown
  requests.
- **Takedown / correction policy:** `[DECIDE: state a simple policy — e.g. an
  outlet or author may request removal of their URLs/derived records from the
  release; describe how to request and the response commitment.]`
- **Responsible disclosure of the framing:** the project is a measurement-validity
  study; any public communication follows the neutrality guardrails in the
  [README](../README.md).
