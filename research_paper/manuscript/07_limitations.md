# 7. Limitations and Threats to Validity

To maintain rigorous scientific transparency, this section explicitly outlines the methodological boundaries, data provenance constraints, and experimental threats to validity governing the reported findings.

---

## 7.1. Image Records versus Biological Specimen Independence

All empirical evaluations in this study were conducted strictly on digital image files ($N = 13,465$) retrieved from public open-access repositories. As documented in Section 3.2, public photographic archives do not provide specimen-level tracking identifiers. Consequently, multiple photographic records may represent burst captures, differing viewpoints, or sequential rotations of the same physical fruit. While perceptual hash auditing at radial thresholds $r \le 8$ identified and excluded near-duplicate files across evaluation tiers (Section 3.6), mathematical hash pruning cannot prove complete biological specimen independence. All reported bootstrap confidence intervals and statistical summaries are strictly conditional on image-level resampling exchangeability.

---

## 7.2. Dataset-Reported Treatment Labels without Independent Chemical Assays

The condition annotations for Cohort B (treatment-labelled known shift) and Cohort C (treatment-labelled unseen shift) rely entirely on metadata published by the FruitVision repository creators [12], who report procuring fruit subjected to formalin preservative immersion. No independent analytical chemistry, gas chromatography–mass spectrometry (GC-MS), high-performance liquid chromatography (HPLC), or destructive tissue assays were performed by the present authors to verify formaldehyde concentration, immersion duration, penetration depth, or residual tissue toxicity. Our findings establish strictly that on this specific dataset-reported cohort, the evaluated post-hoc vision scoring algorithms exhibited weak discrimination between images labelled as treated and natural known-class images; we do not claim to provide a verified chemical assay or toxicological validation.

---

## 7.3. Residual Within-Repository Confounding under Source Matching

Our source-stratified evaluation design (Section 3.4) reduces repository-level provenance differences, while within-repository acquisition variation remains possible. In crowdsourced or field-collected datasets such as FruitVision and Sultana et al., distinct fruit classes may have been photographed across different market stalls, on different calendar dates, under varying solar illumination, or by different field personnel using different handheld mobile cameras. Consequently, subtle background, lighting, or sensor differences between species subsets within a shared repository cannot be entirely ruled out.

---

## 7.4. External Acquisition and Environmental Variability

The external evaluation partitions reflect uncalibrated consumer-grade photography. The images lack radiometric calibration targets, standardized reflectance standards, uniform lux measurements, or controlled illumination geometry. While this unconstrained variability provides a realistic stress test of real-world intake conditions across diverse photographic environments, it limits the ability to isolate specific optical phenomena (e.g., separating surface specular gloss from subsurface light scattering).

---

## 7.5. Statistical Conditioning and Shared Baseline Non-Independence

All reported 95% confidence intervals were generated using non-parametric percentile bootstrap resampling ($B = 1,000$, seed 42) stratified across classes and condition groups. Although Cohorts A--C share the same underlying FruitVision known-class reference records ($N_{\text{id}} = 4,157$), bootstrap resampling was performed independently for each cohort evaluation. Therefore, the marginal confidence intervals should not be interpreted as paired intervals for differences between cohorts. These cohorts are not independent experimental replications, and their point estimates and confidence intervals share an underlying empirical reference sample.

---

## 7.6. Lack of Physical Sorting and Conveyance Validation

This study represents an offline computational benchmark on static digital imagery. The experimental protocol does not evaluate dynamic high-speed conveyor transport, motion blur, variable camera trigger latency, vibrating fruit orientations, or mechanical pneumatic ejection physics. Translating the Dual-Gate decision logic into operational industrial sorting lines will require embedded hardware benchmarking (e.g., NVIDIA Jetson or edge TPU acceleration) and physical pneumatic sorting validation.

---

## 7.7. Algorithmic Implementation Variants

As detailed in Section 4.3, two of the five evaluated post-hoc scoring algorithms represent specific implementation variants rather than exact reproductions of original literature:
1. **ODIN-Style Perturbation Variant:** Canonical ODIN computes perturbations using the cross-entropy gradient with respect to predicted class softmax probabilities. Our implementation evaluates an ODIN-style variant optimizing the sign gradient of the maximum temperature-scaled logit ($T = 1000.0, \varepsilon = 0.0014$), matching the verified execution script.
2. **Modified OpenMax Heuristic:** Our evaluated OpenMax implementation models Weibull tails on 1280-dimensional global pooled features and employs an empirical rank-weighting schedule ($w_{c_r} = 1 - \frac{r-1}{\alpha}(1 - \omega_r)$) that leaves the top-1 predicted logit unaltered ($\alpha = 2, \eta = 20$).

We report results strictly for these verified implementations and do not claim that they represent the theoretical limits of alternative parameterizations.

---

## 7.8. Scale Dependence of the Continuous Margin Proxy

Continuous ROC analysis for the Dual-Gate cascade relies on an exploratory linear margin proxy: $S_{\text{proxy}}(x) = (S_{\text{Energy}}(x) - \tau_E) + (S_{\text{MSP}}(x) - \tau_M)$. Because raw Energy scores are mathematically unbounded on $(-\infty, +\infty)$ with an empirical variance ($\sigma \approx 2.15$) twelve times larger than that of bounded MSP ($\sigma \approx 0.18$), this unweighted linear sum is scale-dependent and dominated by Energy variance. The term $\rho > 0.992$ refers to the empirical Spearman rank correlation between the proxy and raw Energy scores across all 13,465 evaluated image records. All offline operational screening metrics (UFAR, UFAR-Fresh, KRR, Retention) are evaluated strictly using the discrete Boolean conjunction ($g_E(x) \land g_M(x)$) and are immune to proxy scale dependence.
