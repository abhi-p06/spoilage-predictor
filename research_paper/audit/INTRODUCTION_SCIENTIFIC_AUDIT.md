# Scientific and Methodological Audit of Introduction & LaTeX Migration

**Document:** `research_paper/audit/INTRODUCTION_SCIENTIFIC_AUDIT.md`  
**Target Venue:** 5th International Conference on Machine Learning and Data Engineering (ICMLDE 2026) / *Procedia Computer Science* (Elsevier)  
**Lead Auditor:** Senior Scientific Editor & Research Methodologist  
**Audit Date:** November 11, 2026  
**Status:** COMPLETED — ALL CLAIMS DE-CLAIMED AND HARMONIZED WITH FROZEN EVIDENCE  

---

## 1. Executive Summary

This forensic audit evaluates the scientific framing, bibliographic metadata, and empirical claims in Section 1 (Introduction) for the AgriRoute manuscript. Following the transition to the official supplied ICMLDE 2026 LaTeX template as the canonical manuscript source, every material research claim in Section 1 was audited against:
1. `STAGE4_1_2_1_1_FINAL_RESULTS_REPORT.md`
2. `STAGE4_1_2_1_1_FINAL_CLAIMS_LEDGER.csv`
3. `STAGE4_1_2_1_SOURCE_STRATIFIED_CONFIDENCE_INTERVALS.csv`
4. `STAGE4_1_2_1_SOURCE_STRATIFIED_PHASH_SENSITIVITY.csv`
5. `STAGE4_1_IMAGE_LEVEL_PREDICTIONS.csv`
6. `STAGE4_0_3_CORRECTED_THRESHOLD_TABLE.csv`

All unsupported assertions, hyperbolic novelty declarations, conflated agricultural loss statistics, and biological causal inferences have been systematically eliminated or re-scoped.

---

## 2. Itemized Scientific Corrections Ledger

| Category | Prior Unsound / Conflated Formulation | Corrected Formulation | Scientific & Empirical Rationale |
| :--- | :--- | :--- | :--- |
| **A. Agricultural Loss Statistics** | "According to the Food and Agriculture Organization (FAO), approximately one-third of all horticultural produce harvested worldwide is lost or degraded between the farm gate and retail distribution [1]... nationwide surveys in India... range between 6.7% and 15.9% [2]." | FAO 2019 report estimates that approximately 14% of global food production is lost post-harvest up to (excluding) retail. The ICAR-CIPHET (Jha et al., 2015) study is separately cited for Indian commercial fruits with an empirical loss range of 6.70%–15.88% (e.g., apple 10.39%, banana 7.76%, citrus 15.88%). | Conflation of global food waste with regional post-harvest loss violated statistical provenance. FAO (2019) specifically revised its global estimate to ~14% in *The State of Food and Agriculture 2019*, while ICAR-CIPHET 2015 measured distinct Indian commodity chains under an independent sampling design. |
| **B. Preservative & Treatment Shift** | Produce subjected to "chemical fixatives like formalin—intended to retard visual senescence... superficial visual decay symptoms may be artificially masked... conclusively demonstrating that surface vision cannot substitute for biochemical or multi-gas IoT sensing." | Described strictly as a "treatment-labelled condition shift" and a "dataset-reported post-harvest treatment protocol" (10% formalin, 90% water, 30-min immersion, dried, photographed 48h later, documented by Bijoy et al., 2025). | The repository contains RGB photographs with dataset labels; it does not contain analytical chemistry assays (GC-MS, HPLC) or residual formaldehyde concentration measurements. We cannot claim formalin is universally used in commerce or that it inherently conceals decay without per-image chemical testing. |
| **C. Novelty & Research Gap Framing** | Claims of "complete absence of preservative-condition research", "first-ever empirical evidence", "entirely unexplored", and "unprecedented". | Explicitly acknowledges adjacent prior work: Sattar et al. (2024) SensorNet, Bijoy et al. (2025) FruitVision, Wang et al. (2023) unsupervised domain adaptation, Pehlivan & Kara (2026) one-shot open-set food recognition, Jansi & Kavitha (PEOS-Net, 2026), and Yan et al. (PAG-MSBNet, 2026). Narrows research gap to: *A source-stratified empirical evaluation of established post-hoc OOD scores and fixed validation-calibrated rejection behaviour across known-class, unseen-species, treatment-labelled, and combined-shift fruit-image cohorts.* | Prior work exists in agricultural open-set recognition and sensor fusion. Claiming total literature absence is factually inaccurate. AgriRoute's genuine contribution is an empirical evaluation and failure diagnosis of established methods across source-stratified shifts. |
| **D. Benchmark Dataset Claims** | "We curate and publicly release an audited, leak-free evaluation benchmark..." | "We establish an audited image-level evaluation benchmark comprising 13,465 image records... We incorporate exact-duplicate handling and perceptual-hash (pHash) sensitivity analysis across Hamming distance radii $r \in \{0, 4, 8\}$." | "Publicly release" was inaccurate since the underlying datasets belong to third parties under diverse academic licenses. "Leak-free" as an absolute claim is mathematically unsupportable under natural image repetition; pHash sensitivity analysis quantifies the empirical impact of potential near-duplicates. |
| **E. Confounding & Source Matching** | "By benchmarking within shared repositories, we eliminate cross-repository confounding." | "By benchmarking within shared repositories, source matching reduces cross-repository confounding while potential within-repository capture variation remains." | Source stratification controls for differences between repositories (camera optics, ambient studio setup), but cannot eliminate within-repository batch, session, or cultivar variations. |
| **F. Cohort Partitioning Precision** | Partition D1 loosely described as unseen species. | Partition D1 clearly identified as the pooled external unseen-species cohort ($N = 4,776$), distinguished from its repository-specific components: FruitVision D1 ($N = 2,999$, 6 species) and Sultana D1 ($N = 1,777$, 3 species). | Prevents ambiguity between pooled benchmark results and source-matched Cohorts A and D. |
| **G. Terminology: Specimen vs. Image Counts** | "Specimens", "physical fruit specimens". | "Image records", "image count" ($N = 13,465$). | Image repositories often photograph the same physical fruit specimen from multiple viewpoints or lighting conditions. Referring to records as independent biological specimens overstates sample independence. |
| **H. Operational Metrics Precision** | Ambiguous or misstated balanced accuracy and confusion counts. | Balanced accuracy explicitly reported: Partition A = 97.09%, pooled B = 68.66%, FruitVision B = 69.56%, Sultana B = 65.55%. Dual-Gate UFAR on Cohort A: 16.07% at $\tau_{95}$ ($482/2,999$). External known-class Dual-Gate KRR: $\approx 41.98\%$ ($2,246/5,350$). Cohort B Dual-Gate UFAR-Fresh: 42.83% ($821/1,917$). | Matches exact values in `STAGE4_1_2_1_1_FINAL_RESULTS_REPORT.md` and `STAGE4_1_2_1_1_FINAL_CLAIMS_LEDGER.csv`. |
| **I. Dual-Gate Framing** | Continuous linear margin proxy conflated with discrete gate or claimed as a novel model. | Dual-Gate defined as an operational conjunctive rule ($\text{Energy} \le \tau_{\text{Energy}} \land \text{MSP} \ge \tau_{\text{MSP}}$), keeping discrete rejection distinct from its continuous linear margin proxy. Disclaims novelty of the decision rule. | Rejection gates are standard threshold cascades; claiming the linear proxy as a new model is unwarranted. |
| **J. Failure Analysis & Biological Speculation** | Asserting that visual artifacts (russeting, peel striations) causally caused model misclassification. | Framed strictly as qualitative error-analysis observations and diagnostic hypotheses requiring subsequent ablation. | Causal attribution requires controlled visual intervention experiments, which were not performed. |

---

## 3. Bibliographic Integrity & Verification Summary

All 24 citations cited in Section 1 have been programmatically validated against publisher records (CrossRef API and Elsevier/Springer/Nature databases).

### Key Metadata Rectifications:
1. **Chen et al. (2024):** Corrected article number from erroneous draft entry `3214` to authoritative publisher record `3454` (*Scientific Reports*, 14:3454, DOI: `10.1038/s41598-024-53349-w`).
2. **Abayomi-Alli et al. (FruitQ):** Corrected publication date and issue specification from online preprint notice `2023` to official journal volume assignment `2024, Vol. 83, Issue 4, pp. 11433–11460` (DOI: `10.1007/s11042-023-16058-6`).
3. **Primary Data Descriptors Added:** Integrated Sultana et al. (2022, *Data in Brief* 44:108552) and Bijoy et al. (FruitVision, 2025, *Data in Brief* 61:111752).
4. **Adjacent OSR/OOD Works Integrated:** Integrated Sattar et al. (2024), Wang et al. (2023), Pehlivan & Kara (2026), Jansi & Kavitha (PEOS-Net, 2026), and Yan et al. (PAG-MSBNet, 2026).
5. **Procedia Reference Numbering:** Strictly enforced Vancouver bracketed numerical citations (`[1]`, `[2]`, `[3]`) using `\biboptions{sort&compress}` and `\bibliographystyle{elsarticle-num}`.

---

## 4. LaTeX Template & Submission Policy Observations

1. **Procedia Layout Standard:** Verified that the document class `\documentclass[3p,times,procedia]{elsarticle}` enforces the mandatory $192 \times 262\text{ mm}$ single-column geometry with Elsevier CRC header and footer decorations (`ecrc.sty`).
2. **Submission Format Ambiguity:** The conference organizer instructions package includes both a `.docm` Word template and a LaTeX template folder. Authors should confirm with the ICMLDE 2026 program chairs whether the final camera-ready submission permits direct LaTeX PDF submission or requires conversion to Word CRC format. In the interim, LaTeX is adopted as the canonical version-controlled authoring source.

