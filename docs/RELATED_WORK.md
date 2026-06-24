# Related Work — structured map

> **Status:** working draft. This is a **map**, not a literature review in prose —
> four clusters, each with sources and a one-line statement of how this project
> relates. **Every entry is tagged `[VERIFY]`: confirm each citation
> independently before using it.** The citations were gathered and
> cross-checked against authoritative pages (publisher, DOI, arXiv, ACL
> Anthology, WorldCat), but bibliographic details — especially DOI strings on
> publisher pages that block automated access — must be human-verified. Items
> with residual uncertainty carry an extra **⚠** note, and a per-cluster
> *Unresolved / gaps* line records what could not be confirmed or located.

**Clusters**
- [(a) News-diversity metrics & normative frameworks](#a-news-diversity-metrics--normative-frameworks)
- [(b) Measurement validity in computational communication science](#b-measurement-validity-in-computational-communication-science)
- [(c) Cross-system & cross-lingual measurement](#c-cross-system--cross-lingual-measurement)
- [(d) Vietnamese news / NLP datasets & tooling](#d-vietnamese-news--nlp-datasets--tooling)

> **Foundational vs. recent.** Each cluster lists **foundational** anchors first
> — deliberately canonical, often older, and the standard references to keep —
> then a **Recent / SOTA (2022–2026)** block that keeps the methods, tooling, and
> empirical layer current. (Replacing the canonical works with newer ones would
> weaken the paper; the fix for "outdated" is the SOTA block, not deletion.) All
> entries remain `[VERIFY]`.

---

## (a) News-diversity metrics & normative frameworks

**How this project relates:** it *operationalises* these conceptual/normative
diversity frameworks as supply-side metrics and *stress-tests* the recommender-
diversity measures (especially RADio) by re-specifying them from the exposure
setting to the published cross-section.

- **The Unified Framework of Media Diversity: A Systematic Literature Review.** Loecherbach, F., Moeller, J., Trilling, D. & van Atteveldt, W. (2020). *Digital Journalism* 8(5), 605–642. https://doi.org/10.1080/21670811.2020.1764374 — `[VERIFY]`
  - _Relation:_ supplies the integrative variety/balance/disparity vocabulary used to position which "place" in the journalistic information chain this project measures.
- **RADio – Rank-Aware Divergence Metrics to Measure Normative Diversity in News Recommendations.** Vrijenhoek, S., Bénédict, G., Gutierrez Granada, M., Odijk, D. & de Rijke, M. (2022). *RecSys '22*. https://doi.org/10.1145/3523227.3546780 (preprint arXiv:2209.13520) — `[VERIFY]`
  - _Relation:_ the direct methodological template — its calibration/fragmentation/divergence metrics are re-purposed from recommendations to the supply side and are what the study stress-tests.
- **Do Not Blame It on the Algorithm: An Empirical Assessment of Multiple Recommender Systems and Their Impact on Content Diversity.** Möller, J., Trilling, D., Helberger, N. & van Es, B. (2018). *Information, Communication & Society* 21(7), 959–977. https://doi.org/10.1080/1369118X.2018.1444076 — `[VERIFY]`
  - _Relation:_ shows diversity scores depend heavily on operational choices, motivating this project's measurement-validity focus.
- **On the Democratic Role of News Recommenders.** Helberger, N. (2019). *Digital Journalism* 7(8), 993–1012. https://doi.org/10.1080/21670811.2019.1623700 — `[VERIFY]`
  - _Relation:_ supplies the normative typology of news roles that defines *what kind* of diversity each metric is meant to capture (used interpretively, not politically).
- **Exposure Diversity as a Design Principle for Recommender Systems.** Helberger, N., Karppinen, K. & D'Acunto, L. (2018). *Information, Communication & Society* 21(2), 191–207. https://doi.org/10.1080/1369118X.2016.1271900 — `[VERIFY]`
  - _Relation:_ articulates the exposure-side diversity this project explicitly brackets off, sharpening its supply-side boundary.
- **Deconstructing the Diversity Principle.** Napoli, P. M. (1999). *Journal of Communication* 49(4), 7–34. https://doi.org/10.1111/j.1460-2466.1999.tb02815.x — `[VERIFY]`
  - _Relation:_ the source/content/exposure decomposition this project relies on to keep outlet-concentration and topic-diversity metrics separate.
- **Diversity in the News: A Conceptual and Methodological Framework.** Voakes, P. S., Kapfer, J., Kurpius, D. & Chern, D. S.-Y. (1996). *Journalism & Mass Communication Quarterly* 73(3), 582–593. https://doi.org/10.1177/107769909607300306 — `[VERIFY]`
  - _Relation:_ empirically shows source and content diversity diverge — justifying this project's separate reporting and its discriminant-validity check.
- **A General Framework for Analysing Diversity in Science, Technology and Society.** Stirling, A. (2007). *Journal of the Royal Society Interface* 4(15), 707–719. https://doi.org/10.1098/rsif.2007.0213 — `[VERIFY]`
  - _Relation:_ the formal variety/balance/disparity heuristic underpinning the entropy/Gini/Simpson and disparity-aware computations in METHODOLOGY §2.
- **On Competition, Access and Diversity in Media, Old and New.** van Cuilenburg, J. (1999). *New Media & Society* 1(2), 183–207. https://doi.org/10.1177/14614449922225555 — `[VERIFY]`
  - _Relation:_ links market structure/concentration to media diversity, informing the use of `outlet_type` as a structural covariate against concentration measures.
- **Media Performance: Mass Communication and the Public Interest.** McQuail, D. (1992). *Sage*. ISBN 9780803982949 — WorldCat: https://search.worldcat.org/title/27888643 — `[VERIFY]` ⚠ monograph: ISBN/WorldCat record, not a DOI.
  - _Relation:_ the canonical statement of diversity as a public-interest performance criterion — the normative baseline against which the project asks whether the *metrics* still mean anything elsewhere.
- **News Diversity Reconsidered: A Systematic Literature Review Unraveling the Diversity in Conceptualizations.** Joris, G., De Grove, F., Van Damme, K. & De Marez, L. (2020). *Journalism Studies* 21(13), 1893–1912. https://doi.org/10.1080/1461670X.2020.1797527 — `[VERIFY]`
  - _Relation:_ documents the inconsistency of diversity dimensions, reinforcing the project's insistence on making metric/conceptual choices explicit before cross-system application.

**Recent / SOTA (2022–2026):**

- **RADio\* – An Introduction to Measuring Normative Diversity in News Recommendations.** Vrijenhoek, S., Bénédict, G., Gutierrez Granada, M. & Odijk, D. (2024). *ACM Transactions on Recommender Systems*. https://doi.org/10.1145/3636465 — `[VERIFY]`
  - _Relation:_ the extended journal reference for the RADio metric definitions the project re-specifies to the supply side — cite as the current statement of those metrics.
- **Diversity of What? On the Different Conceptualizations of Diversity in Recommender Systems.** Vrijenhoek, S., Daniil, S., Sandel, J. & Hollink, L. (2024). *ACM FAccT 2024*. arXiv:2405.02026 — `[VERIFY]`
  - _Relation:_ disambiguates competing diversity constructs, helping the project state precisely which construct each supply-side metric captures.
- **Measuring Variety, Balance, and Disparity: An Analysis of Media Coverage of the 2021 German Federal Election.** Färber, M., Schwade, J. & Jatowt, A. (2023). *arXiv*. arXiv:2308.03531 — `[VERIFY]`
  - _Relation:_ a close supply-side precedent operationalising Stirling's variety/balance/disparity across many outlets — a direct methodological comparator.
- **Exploring the Link Between Media Concentration and News Content Diversity Using Automated Text Analysis.** Hendrickx, J. & Van Remoortere, A. (2024). *Journalism* 25(2), 353–371. https://doi.org/10.1177/14648849221136946 — `[VERIFY]`
  - _Relation:_ recent supply-side measurement of cross-title content overlap — a direct analogue for the cross-outlet agenda-overlap metrics.
- **Benefits of Diverse News Recommendations for Democracy: A User Study.** Heitz, L., Lischka, J. A., Birrer, A., Paudel, B., Tolmeijer, S., Laugwitz, L. & Bernstein, A. (2022). *Digital Journalism* 10(10), 1710–1730. https://doi.org/10.1080/21670811.2021.2021804 — `[VERIFY]`
  - _Relation:_ a recent exposure-side normative-diversity study — cited to mark the boundary the project does not cross (supply-side only).

**Unresolved / gaps:** none failed verification in this cluster. A dedicated
treatment of *outlet/source* concentration measures from media economics (HHI,
CRk) is referenced operationally in METHODOLOGY but not yet cited here —
`[VERIFY/ADD: a canonical media-economics concentration reference if a reviewer
expects one.]`

---

## (b) Measurement validity in computational communication science

**How this project relates:** it is a concrete instance of this agenda — treating
diversity metrics as instruments and subjecting them to content, convergent/
discriminant, and contextual validity checks plus baseline (null) testing.

- **Text as Data: The Promise and Pitfalls of Automatic Content Analysis Methods for Political Texts.** Grimmer, J. & Stewart, B. M. (2013). *Political Analysis* 21(3), 267–297. https://doi.org/10.1093/pan/mps028 — `[VERIFY]`
  - _Relation:_ the field-defining injunction to validate (not assume) automated measures, which this study operationalises for diversity metrics.
- **Measurement Validity: A Shared Standard for Qualitative and Quantitative Research.** Adcock, R. & Collier, D. (2001). *American Political Science Review* 95(3), 529–546. https://doi.org/10.1017/S0003055401003100 — `[VERIFY]`
  - _Relation:_ supplies the validity vocabulary (content, convergent/discriminant, contextual) the project's analyses are organised around.
- **When Communication Meets Computation: Opportunities, Challenges, and Pitfalls in Computational Communication Science.** van Atteveldt, W. & Peng, T.-Q. (2018). *Communication Methods and Measures* 12(2–3), 81–92. https://doi.org/10.1080/19312458.2018.1458084 — `[VERIFY]`
  - _Relation:_ frames cross-context transfer of computational methods as a central problem — exactly this study's setting.
- **Three Gaps in Computational Text Analysis Methods for Social Sciences: A Research Agenda.** Baden, C., Pipal, C., Schoonvelde, M. & van der Velden, M. A. C. G. (2022). *Communication Methods and Measures* 16(1), 1–18. https://doi.org/10.1080/19312458.2021.2015574 — `[VERIFY]`
  - _Relation:_ names under-attention to validity and English-language bias as field gaps; the project targets both on a Vietnamese corpus.
- **In Validations We Trust? The Impact of Imperfect Human Annotations as a Gold Standard on the Quality of Validation of Automated Content Analysis.** Song, H., et al. (2020). *Political Communication* 37(4), 550–572. https://doi.org/10.1080/10584609.2020.1723752 — `[VERIFY]` ⚠ confirm the full author list before citing "et al.".
  - _Relation:_ shows validation is itself error-prone, motivating reliance on convergent metrics and shuffled/random baselines over a single gold standard.
- **Adapting Computational Text Analysis to Social Science (and Vice Versa).** DiMaggio, P. (2015). *Big Data & Society* 2(2), 1–5. https://doi.org/10.1177/2053951715602908 — `[VERIFY]`
  - _Relation:_ the "adapt, don't apply off-the-shelf" logic that this project tests as metric re-specification.
- **How to Analyze Political Attention with Minimal Assumptions and Costs.** Quinn, K. M., Monroe, B. L., Colaresi, M., Crespin, M. H. & Radev, D. R. (2010). *American Journal of Political Science* 54(1), 209–228. https://doi.org/10.1111/j.1540-5907.2009.00427.x — `[VERIFY]`
  - _Relation:_ a canonical topic-model-for-attention application whose validation practice and topic-count sensitivity inform the project's parameter-sensitivity analysis.
- **Reading Tea Leaves: How Humans Interpret Topic Models.** Chang, J., Boyd-Graber, J., Gerrish, S., Wang, C. & Blei, D. M. (2009). *NeurIPS 22*, 288–296. https://proceedings.neurips.cc/paper/2009/file/f92586a25bb3145facd64ab20fd554ff-Paper.pdf — `[VERIFY]`
  - _Relation:_ shows statistical fit and human interpretability of topics can diverge — underpinning the project's treatment of topic quality as a validity question.
- **Taking Stock of the Toolkit: An Overview of Relevant Automated Content Analysis Approaches and Techniques for Digital Journalism Scholars.** Boumans, J. W. & Trilling, D. (2016). *Digital Journalism* 4(1), 8–23. https://doi.org/10.1080/21670811.2015.1096598 — `[VERIFY]`
  - _Relation:_ situates the diversity-metric toolkit within journalism studies and stresses fit-to-purpose method choice.
- **Reliability in Content Analysis: Some Common Misconceptions and Recommendations.** Krippendorff, K. (2004). *Human Communication Research* 30(3), 411–433. https://doi.org/10.1111/j.1468-2958.2004.tb00738.x — `[VERIFY]` ⚠ DOI string not click-through-confirmed (publisher blocked automated access); all other fields firm.
  - _Relation:_ the reliability standards the project treats as a precondition for, and complement to, the validity of derived measures.
- **A Roadmap for Computational Communication Research.** van Atteveldt, W., Margolin, D., Shen, C., Trilling, D. & Weber, R. (2019). *Computational Communication Research* 1(1), 1–11. https://doi.org/10.5117/CCR2019.1.001.VANA — `[VERIFY]`
  - _Relation:_ articulates the transparency/reproducibility/risky-result agenda matching the project's reproducible-pipeline + baseline-testing stance (and its target venue).

**Recent / SOTA (2022–2026) — LLM-based measurement and its validity:**

- **ChatGPT Outperforms Crowd Workers for Text-Annotation Tasks.** Gilardi, F., Alizadeh, M. & Kubli, M. (2023). *PNAS* 120(30), e2305016120. https://doi.org/10.1073/pnas.2305016120 (arXiv:2303.15056) — `[VERIFY]`
  - _Relation:_ a benchmark motivating an optional LLM-based topic/annotation arm — while reinforcing that any such measure still needs task-specific validation.
- **Can Large Language Models Transform Computational Social Science?** Ziems, C., Held, W., Shaikh, O., Chen, J., Zhang, Z. & Yang, D. (2024). *Computational Linguistics* 50(1), 237–291. https://doi.org/10.1162/coli_a_00502 (arXiv:2305.03514) — `[VERIFY]`
  - _Relation:_ the field-level framing for where LLM-based measurement is (and is not) trustworthy in computational social science.
- **Best Practices for Text Annotation with Large Language Models.** Törnberg, P. (2024). *Sociologica* 18(2), 67–85. https://doi.org/10.6092/issn.1971-8853/19461 (arXiv:2402.05129) — `[VERIFY]`
  - _Relation:_ the procedural standard (prompt-stability, validation against human labels) the project would follow for any LLM-derived layer.
- **Automated Annotation with Generative AI Requires Validation.** Pangakis, N., Wolken, S. & Fasching, N. (2023). *arXiv*. arXiv:2306.00176 — `[VERIFY]`
  - _Relation:_ supplies the central validity rule — validate LLM annotations task-by-task against human labels rather than assuming transfer.
- **Testing the Reliability of ChatGPT for Text Annotation and Classification: A Cautionary Remark.** Reiss, M. V. (2023). *arXiv*. arXiv:2304.11085 — `[VERIFY]`
  - _Relation:_ documents prompt-sensitivity and non-determinism, reinforcing the project's parameter-sensitivity and stability checks.
- **The Dangers of Using Proprietary LLMs for Research.** Ollion, É., Shen, R., Macanovic, A. & Vanhée, A. (2024). *Nature Machine Intelligence* 6, 4–5. https://doi.org/10.1038/s42256-023-00783-6 — `[VERIFY]`
  - _Relation:_ grounds reproducibility caveats (closed-model drift, access) for any LLM-derived measure.
- **GPT Is an Effective Tool for Multilingual Psychological Text Analysis.** Rathje, S., Mirea, D.-M., Sucholutsky, I., Marjieh, R., Robertson, C. E. & Van Bavel, J. J. (2024). *PNAS* 121(34), e2308950121. https://doi.org/10.1073/pnas.2308950121 — `[VERIFY]`
  - _Relation:_ evidence that LLM-based measurement can hold across many languages — motivating, but not presuming, validity testing in the Vietnamese setting.
- **Large Language Models as a Substitute for Human Experts in Annotating Political Text.** Heseltine, M. & Clemm von Hohenberg, B. (2024). *Research & Politics* 11(1). https://doi.org/10.1177/20531680241236239 — `[VERIFY]`
  - _Relation:_ a cross-country convergent-validity test of LLM annotation that parallels the project's convergent-validity design in a new linguistic context.

**Unresolved / gaps:** Song et al. (2020) author list abbreviated — expand
before citing. Krippendorff DOI flagged above.

---

## (c) Cross-system & cross-lingual measurement

**How this project relates:** it sits at the intersection — applying a Western
media-systems lens to a non-Western case, and depending on multilingual NLP whose
own cross-lingual validity is itself part of the literature being tested.

- **Comparing Media Systems: Three Models of Media and Politics.** Hallin, D. C. & Mancini, P. (2004). *Cambridge University Press*. ISBN 9780521543088 — https://www.cambridge.org/core/books/comparing-media-systems/F61C2EF4D8120ED1F37D013E96E9A87B — `[VERIFY]`
  - _Relation:_ the canonical media-systems typology behind characterising outlets by structural type; the project tests whether metrics built in this Western-derived frame transfer.
- **Comparing Media Systems Beyond the Western World.** Hallin, D. C. & Mancini, P. (eds.) (2012). *Cambridge University Press*. ISBN 9781107699540 — https://www.cambridge.org/core/books/comparing-media-systems-beyond-the-western-world/1DBEDE293709F5588E53C3CC7CBCDB50 — `[VERIFY]` ⚠ book DOI (10.1017/CBO9781139005098) follows Cambridge's scheme but use the Cambridge Core URL as the stable anchor.
  - _Relation:_ directly motivates the validity question — how far Western media-system concepts travel — at the metric level for Vietnam.
- **Comparing Political Journalism.** de Vreese, C., Esser, F. & Hopmann, D. N. (eds.) (2017). *Routledge*. ISBN 9781138655867 — https://www.routledge.com/Comparing-Political-Journalism/de-Vreese-Esser-Hopmann/p/book/9781138655867 — `[VERIFY]`
  - _Relation:_ situates this single-system supply-diversity study within the comparative-content tradition.
- **Reproducible Extraction of Cross-lingual Topics (rectr).** Chan, C.-H., Zeng, J., Wessler, H., Jungblut, M., Welbers, K., Bajjalieh, J. W., Althaus, S. & van Atteveldt, W. (2020). *Communication Methods and Measures* 14(4), 285–305. https://doi.org/10.1080/19312458.2020.1812555 — `[VERIFY]`
  - _Relation:_ a directly comparable communication-science method for embedding-based cross-lingual topic alignment, which this project's cross-lingual same-story/topic work builds on and tests on Vietnamese.
- **Cross-Lingual Classification of Political Texts Using Multilingual Sentence Embeddings.** Licht, H. (2023). *Political Analysis* 31(3), 366–379. https://doi.org/10.1017/pan.2022.29 — `[VERIFY]`
  - _Relation:_ validates multilingual sentence embeddings as a language-independent representation — the core technique behind the project's cross-lingual near-duplicate detection.
- **Making Monolingual Sentence Embeddings Multilingual using Knowledge Distillation.** Reimers, N. & Gurevych, I. (2020). *EMNLP 2020*, 4512–4525. https://aclanthology.org/2020.emnlp-main.365/ — `[VERIFY]`
  - _Relation:_ the authoritative method behind the `paraphrase-multilingual-MiniLM-L12-v2` model used for cross-lingual deduplication.
- **Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks.** Reimers, N. & Gurevych, I. (2019). *EMNLP-IJCNLP 2019*, 3982–3992. https://aclanthology.org/D19-1410/ (arXiv:1908.10084) — `[VERIFY]`
  - _Relation:_ the foundational architecture of the sentence-transformers family the dedup pass depends on (cited by the chosen model's card).
- **Greasing the Wheels for Comparative Communication Research: Supervised Text Classification for Multilingual Corpora.** Lind, F., Heidenreich, T., Kralj, C. & Boomgaarden, H. G. (2021). *Computational Communication Research* 3(3), 1–25. https://doi.org/10.5117/CCR2021.3.001.LIND — `[VERIFY]`
  - _Relation:_ establishes validated multilingual text workflows in communication research — the methodological backdrop for assessing metric validity on Vietnamese news.
- **Machine Translation vs. Multilingual Dictionaries: Assessing Two Strategies for the Topic Modeling of Multilingual Text Collections.** Maier, D., Baden, C., Stoltenberg, D., de Vries-Kedem, M. & Waldherr, A. (2022). *Communication Methods and Measures* 16(1), 19–38. https://doi.org/10.1080/19312458.2021.1955845 — `[VERIFY]`
  - _Relation:_ flags where translation/representation choices affect cross-lingual topic-model validity, informing the project's preprocessing decisions.
- **Multilingual Sentiment Analysis: A New Approach to Measuring Conflict in Legislative Speeches.** Proksch, S.-O., Lowe, W., Wäckerle, J. & Soroka, S. (2019). *Legislative Studies Quarterly* 44(1), 97–131. https://doi.org/10.1111/lsq.12218 — `[VERIFY]`
  - _Relation:_ a widely-cited demonstration that multilingual measures can be made comparable, supporting the premise that Western-developed measures need explicit cross-lingual validation.

**Recent / SOTA (2019–2026):**

- **Rethinking Hallin and Mancini Beyond the West: An Analysis of Media Systems in Central and Eastern Europe.** Castro Herrero, L., Humprecht, E., Engesser, S., Brüggemann, M. & Büchel, F. (2017). *International Journal of Communication* 11, 4797–4823. https://ijoc.org/index.php/ijoc/article/view/6035 — `[VERIFY]` ⚠ 2017, just outside the "recent" window but the cleanest empirical beyond-the-West re-specification example.
  - _Relation:_ an empirical example of re-clustering the Hallin–Mancini dimensions outside the original cases — the comparative analogue of asking whether established constructs behave sensibly in a new system.
- **Protecting Democracy or Conspiring Against It? Media and Politics in Latin America.** de Albuquerque, A. (2019). *Journalism* 20(7), 906–923. https://doi.org/10.1177/1464884917738376 — `[VERIFY]`
  - _Relation:_ a critique of transplanting Western press–politics categories non-West, supporting the argument for metric re-specification rather than assumed transfer.
- **Hybrid Media and Hybrid Politics: Contesting Informational Uncertainty in Lebanon and Tunisia.** Voltmer, K., Selvik, K. & Høigilt, J. (2021). *The International Journal of Press/Politics* 26(4), 842–860. https://doi.org/10.1177/1940161221999266 — `[VERIFY]`
  - _Relation:_ recent non-Western media-systems framing that supports describing outlet structural types neutrally as covariates rather than against a Western baseline.
- **Online Media Communication Research in Vietnam 2003–2023: A Review.** Triệu, L., Do, P. & Nguyen, N. (2024). *Online Media and Global Communication* 3(3), 447–471. https://doi.org/10.1515/omgc-2024-0034 — `[VERIFY]`
  - _Relation:_ locates the project within existing Vietnamese online-media scholarship and helps establish the supply-side measurement gap it addresses.
- **Who Attacks, and Why? Using LLMs to Identify Negative Campaigning across 19 Countries.** Hartman, V. & Törnberg, P. (2025). *arXiv*. arXiv:2507.17636 — `[VERIFY]` ⚠ preprint — confirm status before citing.
  - _Relation:_ a cross-lingual LLM-measurement case (zero-shot across ten languages) relevant to the project's multilingual processing beyond Western languages.

**Unresolved / gaps:** a Lind/Eberl-style "validating multilingual computational
text analysis" framework piece surfaced repeatedly but could not be
bibliographically confirmed — `[VERIFY/ADD: locate and confirm if wanted.]` Book
DOIs anchored to Cambridge Core URLs as noted. Additional peer-reviewed sources
characterising the Vietnamese media structure exist but carry politically loaded
*titles* (e.g. Haenig & Ji 2024, https://doi.org/10.1007/s44216-024-00024-6;
Luong Le & Block 2024, https://doi.org/10.1177/2046147X231218310; Mattsson 2022,
https://doi.org/10.1080/1461670X.2022.2098169) — `[DECIDE: whether to cite any of
these for the outlet-type / structural covariate given the neutral, low-profile
framing; if cited, keep the in-text framing strictly structural.]`

---

## (d) Vietnamese news / NLP datasets & tooling

**How this project relates:** it *uses* these toolkits/models and *complements*
these task-specific corpora — positioning itself as reusable cross-outlet
supply-side measurement infrastructure, not "the first Vietnamese news dataset."
(Sentence-BERT and the multilingual embedding method are in cluster (c).)

- **VnCoreNLP: A Vietnamese Natural Language Processing Toolkit.** Vu, T., Nguyen, D. Q., Nguyen, D. Q., Dras, M. & Johnson, M. (2018). *NAACL-HLT 2018: Demonstrations*, 56–60. https://aclanthology.org/N18-5012/ (code: https://github.com/vncorenlp/VnCoreNLP) — `[VERIFY]`
  - _Relation:_ a standard Vietnamese segmentation/POS/NER pipeline — an alternative segmenter and word-boundary reference for the sensitivity checks.
- **PhoBERT: Pre-trained Language Models for Vietnamese.** Nguyen, D. Q. & Nguyen, A. T. (2020). *Findings of EMNLP 2020*, 1037–1042. https://aclanthology.org/2020.findings-emnlp.92/ (DOI 10.18653/v1/2020.findings-emnlp.92; code: https://github.com/VinAIResearch/PhoBERT) — `[VERIFY]`
  - _Relation:_ the standard Vietnamese pretrained encoder — the contextual-embedding option for topic assignment / near-duplicate detection and an embedding-model sensitivity arm.
- **underthesea — Vietnamese NLP Toolkit.** undertheseanlp (software, Apache-2.0). https://github.com/undertheseanlp/underthesea — `[VERIFY]` ⚠ no canonical paper found — cite as software with URL + access date.
  - _Relation:_ the Phase-1 word segmenter; supplies the tokenisation required before any token-based metric.
- **pyvi — Python Vietnamese Core NLP Toolkit.** Tran, V.-T. (software, MIT). https://github.com/trungtv/pyvi (PyPI: https://pypi.org/project/pyvi/) — `[VERIFY]`
  - _Relation:_ the alternative CRF-based segmenter named in the preprocessing stack (segmenter sensitivity check).
- **VNTC: A Large-scale Vietnamese News Text Classification Corpus.** Hoang, C. D. V., Dinh, D., Nguyen, L. N. & Ngo, Q. H. (corpus, MIT) — https://github.com/duyvuleo/VNTC; assoc. paper "A Comparative Study on Vietnamese Text Classification Methods," *RIVF 2007*, DOI 10.1109/RIVF.2007.369167 — `[VERIFY]` ⚠ IEEE DOI cross-confirmed, not click-through (JS-gated) — verify on IEEE.
  - _Relation:_ an existing topic-labelled Vietnamese news corpus — a comparison point that frames this project as cross-outlet diversity infrastructure rather than another classification set.
- **UIT-VSFC: Vietnamese Students' Feedback Corpus.** Nguyen, K. V., Nguyen, V. D., Nguyen, P. X.-V., Truong, T. T.-H. & Nguyen, N. L.-T. (2018). *KSE 2018*. DOI 10.1109/KSE.2018.8573337 (data: https://github.com/kietnv/uit-vsfc; https://huggingface.co/datasets/uitnlp/vietnamese_students_feedback) — `[VERIFY]` ⚠ IEEE DOI cross-confirmed, not click-through.
  - _Relation:_ a widely-used UIT-group Vietnamese corpus illustrating established annotation/benchmark practice the datasheet can align with.
- **ViNLI: A Vietnamese Corpus for Studies on Open-Domain Natural Language Inference.** Huynh, T. V., Nguyen, K. V. & Nguyen, N. L.-T. (2022). *COLING 2022*, 3858–3872. https://aclanthology.org/2022.coling-1.339/ — `[VERIFY]`
  - _Relation:_ built from 800+ online news articles across 13 topics — a direct precedent for sampling Vietnamese news by topic and a comparison for topic-coverage structure.
- **paraphrase-multilingual-MiniLM-L12-v2.** sentence-transformers (Reimers & Gurevych) (model). https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 — `[VERIFY]`
  - _Relation:_ the specific 50+-language embedding model used for cross-outlet near-duplicate/same-story detection (method refs in cluster (c)).
- **Learning Word Vectors for 157 Languages (fastText).** Grave, E., Bojanowski, P., Gupta, P., Joulin, A. & Mikolov, T. (2018). *LREC 2018*. Vectors: https://fasttext.cc/docs/en/crawl-vectors.html — `[VERIFY]`
  - _Relation:_ distributes pretrained Vietnamese static word vectors — a baseline representation option for Vietnamese content.

**Recent / SOTA (2022–2026) — embeddings, benchmarks & Vietnamese LMs:**

- **Multilingual E5 Text Embeddings.** Wang, L., Yang, N., Huang, X., Yang, L., Majumder, R. & Wei, F. (2024). *arXiv / model*. arXiv:2402.05672 (model: https://huggingface.co/intfloat/multilingual-e5-large-instruct) — `[VERIFY]`
  - _Relation:_ a primary SOTA multilingual embedder — the leading alternative to MiniLM for the cross-outlet near-duplicate step and the embedding-sensitivity arm.
- **BGE M3-Embedding: Multi-Lingual, Multi-Functionality, Multi-Granularity Text Embeddings.** Chen, J., Xiao, S., Zhang, P., Luo, K., Lian, D. & Liu, Z. (2024). *Findings of ACL 2024*, 2318–2335. https://aclanthology.org/2024.findings-acl.137/ (arXiv:2402.03216; model: https://huggingface.co/BAAI/bge-m3) — `[VERIFY]`
  - _Relation:_ a second SOTA multilingual representation (long-context) for the embedding-robustness comparison.
- **Language-agnostic BERT Sentence Embedding (LaBSE).** Feng, F., Yang, Y., Cer, D., Arivazhagan, N. & Wang, W. (2022). *ACL 2022*. arXiv:2007.01852 — `[VERIFY]`
  - _Relation:_ an established cross-lingual sentence encoder — a natural older baseline alongside MiniLM in the representation-robustness check.
- **mGTE: Generalized Long-Context Multilingual Text Representation and Reranking.** Zhang, X., Zhang, Y., Long, D., Xie, W., et al. (2024). *arXiv / model*. arXiv:2407.19669 (model: https://huggingface.co/Alibaba-NLP/gte-multilingual-base); cf. **jina-embeddings-v3** (Sturua et al., 2024, arXiv:2409.10173) — `[VERIFY]`
  - _Relation:_ additional efficient long-context multilingual encoders to widen the embedding-sensitivity sweep.
- **MTEB / MMTEB — (Massive) Multilingual Text Embedding Benchmark.** Muennighoff, N., Tazi, N., Magne, L. & Reimers, N. (2023, *EACL*, arXiv:2210.07316); Enevoldsen, K., et al. (2025, *MMTEB*, arXiv:2502.13595) — `[VERIFY]`
  - _Relation:_ the standard benchmarks used to justify the embedding-model choice for the representation layer.
- **VN-MTEB: Vietnamese Massive Text Embedding Benchmark.** Pham, et al. (2025). *arXiv*. arXiv:2507.21500 — `[VERIFY]` ⚠ recent preprint — confirm authors/status.
  - _Relation:_ a directly relevant Vietnamese embedding benchmark for empirically selecting/validating the embedding model used in cross-outlet detection.
- **CafeBERT & VLUE: A Benchmark and Multi-task Transfer Learning for Vietnamese NLU.** Do, P., Tran, S., Hoang, P., Nguyen, K. & Nguyen, N. (2024). *Findings of NAACL 2024*. arXiv:2403.15882 — `[VERIFY]`
  - _Relation:_ a recent Vietnamese-adapted XLM-R encoder + NLU benchmark — supports the monolingual-vs-multilingual representation decision.
- **ViDeBERTa: A Powerful Pre-trained Language Model for Vietnamese.** Tran, C., Pham, N., Nguyen, P., Hy, T. & Vu, T. (2023). *Findings of EACL 2023*. https://aclanthology.org/2023.findings-eacl.79/ (arXiv:2301.10439) — `[VERIFY]`
  - _Relation:_ a recent Vietnamese encoder — a monolingual representation baseline in the Vietnamese-NLP context.
- **Recent Vietnamese generation / seq2seq models.** BARTpho (Tran et al., 2022, arXiv:2109.09701); ViT5 (Phan et al., 2022, *NAACL SRW*, arXiv:2205.06457); PhoGPT (Nguyen et al., 2023, arXiv:2311.02945) — `[VERIFY]`
  - _Relation:_ the current Vietnamese pretrained-model landscape, cited to situate representation choices beyond PhoBERT.

**Unresolved / gaps:** underthesea lacks a citable paper (software cite). IEEE
DOIs (VNTC/RIVF 2007; UIT-VSFC/KSE 2018) need a final IEEE click-through.
`[VERIFY/ADD: a Vietnamese *news* topic/dedup dataset closer to this corpus, if
one exists, beyond the classification/NLI corpora above.]` No single canonical
Vietnamese SBERT / bi-encoder checkpoint could be verified to a stable maintainer
— `[VERIFY/ADD: confirm a specific Hugging Face Vietnamese embedding checkpoint
(e.g. a bkai-foundation-models or keepitreal model) before citing.]`

---

## Cross-cutting positioning (one paragraph)

This project (i) takes diversity-metric concepts from **(a)** and computes them
supply-side; (ii) executes the validation imperative of **(b)** by testing those
metrics' interpretability, robustness, convergent validity, and signal-vs-null
behaviour; (iii) places the case in the comparative/cross-lingual frame of
**(c)**, where Western-derived constructs and multilingual NLP both require
explicit transfer validation; and (iv) builds on the Vietnamese tooling and
complements the task-specific corpora of **(d)** as reusable measurement
infrastructure. The gap it fills: established news-diversity metrics have rarely
been **validated as measurements** on a structurally different, non-Western,
non-English media system — and never, to our knowledge, with syndication-aware
supply-side re-specification. This currency matters: 2023–2026 work shows
LLM-based text measurement can rival human coding yet still demands task-specific
validation — sharpening rather than dissolving the validity question the project
addresses. `[VERIFY: this novelty claim with a final targeted
search before the preprint.]`
