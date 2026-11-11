# 6. Discussion

The empirical findings from our source-stratified benchmark carry important implications for agricultural computer vision, out-of-distribution detection, and automated post-harvest sorting workflows. In this section, we analyze the structural drivers of external domain collapse, the weak discrimination observed on dataset-reported treatment labels, the potential operational trade-offs of conservative rejection gating, and prospective engineering pathways for multi-sensor quality assessment.

---

## 6.1. Domain Collapse and the Brittle Nature of Laboratory Vision Models

A central finding of this study is the marked performance collapse of the frozen MobileNetV2 classifier when transitioned from curated laboratory test data (Partition A, 96.92% accuracy) to external repository environments (Partition B, 68.36% accuracy, representing a 28.56 percentage-point degradation). Both external evaluation subsets independently demonstrate this ceiling: 69.14% on FruitVision B and 65.63% on Sultana B.

Crucially, this degradation is not distributed uniformly across classes. As documented in Section 5.2, the classifier exhibits an asymmetric vulnerability on Fresh Apples, collapsing to 32.12% top-1 accuracy (310/965 correct across pooled Partition B). In pooled Partition B, the model misclassifies 40.73% of fresh apples as Rotten Apple (393 images) and 26.42% as Rotten Orange (255 images). Within the FruitVision B subset alone, 345 fresh apples are predicted as Rotten Apple and 242 as Rotten Orange out of 765 images. Qualitative visual inspection indicates that external photographic records frequently exhibit natural surface striations, lenticel spots, and varietal russeting. In contrast, the laboratory-curated Kaggle training distribution consists predominantly of smooth, uniformly illuminated, blemish-free fruit against neutral planar backgrounds. While this visual comparison suggests that surface texture variations may contribute to false-decay classifications, we distinguish this qualitative observation from a formally tested causal mechanism.

This failure mode highlights a pervasive vulnerability in agricultural computer vision literature: benchmark evaluations conducted solely within closed, laboratory-collected datasets create an impression of near-perfect accuracy (often exceeding 95% to 99%) that degrades substantially when models confront external real-world distribution shifts.

---

## 6.2. Weak Discrimination on Dataset-Reported Treatment Labels

Under Cohort B, where identical known species (apple, banana, orange) are evaluated under dataset-reported treatment labels (formalin preservative immersion condition), all five evaluated post-hoc scoring algorithms exhibit weak or near-chance discrimination: Energy AUROC is 53.13% [52.16%, 54.09%], the Energy–MSP linear-margin proxy (exploratory) is 53.96% [52.96%, 54.91%], MSP is 58.77%, and Ledoit--Wolf Mahalanobis distance falls to 47.91%, with retrospective false positive rates exceeding 91% to 98%.

Under the locked prospective operating thresholds ($\tau_{95}$), 821 out of 1,917 dataset-reported treatment-labelled images (42.83% [41.26%, 44.34%]) are accepted by the Dual-Gate and assigned one of the classifier's Fresh-class output labels. Standalone Energy exhibits an even higher rate of acceptance and assignment to Fresh-class output labels of 44.03% (844/1,917).

We emphasize that this study evaluated digital photographic image records bearing repository-assigned labels; we did not perform chemical or toxicological assays to independently verify chemical immersion, confirm compound presence, or quantify tissue residue. Furthermore, our image-based evaluation cannot determine whether biochemical differences manifested as detectable optical features in the evaluated photographs. The empirical finding establishes strictly that within this specific dataset-reported cohort, the evaluated post-hoc vision scoring algorithms did not reliably separate images recorded under the reported treatment protocol from natural known-class fruit. While external RGB photography records visible surface reflectance, this evaluation does not support universal assertions regarding RGB imaging capabilities; rather, on this evaluated dataset-reported cohort, the tested post-hoc visual gates did not provide an effective safeguard against produce carrying treatment labels.

---

## 6.3. Operational Trade-offs: The Potential Economic Overhead of Abstention

Our findings illustrate the divergence between continuous discrimination metrics (AUROC) and the practical demands of operational decision gating. While threshold-independent AUROC indicates partial semantic separation on FruitVision (81.57% for Energy), implementing a prospective operational gate under locked validation thresholds ($\tau_{95}$) reveals a substantial abstention overhead.

Operating thresholds calibrated to accept 95.15% of primary in-distribution validation images exhibit an offline operational Known-Class Rejection Rate (KRR) of 41.98% on FruitVision B and 44.01% on Sultana B (42.43% pooled across Partition B). In practical sorting environments, rejecting over four out of ten known-class items represents a high abstention rate with potential operational consequences: routing 42.43% of known-class image records to manual secondary inspection could potentially increase staffing requirements and reduce line throughput, though physical throughput and financial costs were not directly measured in this offline study.

Furthermore, on Cohort D (Sultana Semantic Shift), offline false acceptance rises to 34.90% for Dual-Gate (with 22.65% accepted and assigned one of the classifier's Fresh-class output labels) alongside a 44.01% KRR. As an untested observational hypothesis, visual commonalities among spherical green fruit classes (such as guava and jujube in Sultana D1 and green apples or citrus in the known set) may relate to this difficulty; however, this morphological resemblance was not causally verified, and no dedicated latent embedding-overlap analysis was performed. These results show that, under the locked thresholds, the evaluated score-based gate did not reliably reject all unseen-species records in Cohort D. The underlying score-distribution and feature-space overlap were not independently quantified.

---

## 6.4. Architectural Comparison: Post-Hoc Scoring Paradigms

Comparing the post-hoc detection mechanisms reveals clear structural distinctions:
1. **Energy vs. Posterior Probability (MSP):** Across both semantic shift cohorts (Cohorts A and D), Energy-based scoring outperforms standard MSP, improving AUROC from 72.42% to 81.57% on FruitVision (+9.15 pp) and from 59.77% to 67.52% on Sultana (+7.75 pp). This is consistent with findings that computing the log-sum-exp over unnormalized logits avoids the probability saturation and artificially overconfident posteriors induced by softmax normalization on out-of-distribution inputs [18].
2. **Penultimate Feature Modeling (Mahalanobis):** Ledoit--Wolf Mahalanobis distance achieves competitive discrimination on semantic shifts (81.41% in A, 68.15% in D). By modeling class-conditional Gaussian clusters in 1280-dimensional feature space, it captures spatial outlier geometry. However, on treatment shift (Cohort B), Mahalanobis distance drops to 47.91% AUROC. This outcome is consistent with weak separation under the evaluated regularized Mahalanobis scoring function. We emphasize that feature-space geometry and cluster overlap were not independently quantified via embedding distances or density estimation; hence, AUROC performance alone cannot be used to infer the exact topological configuration of representations in latent space.
3. **Operational Dual-Gate Behavior:** The joint Boolean conjunction rule ($S_{\text{Energy}} \ge \tau_E \land S_{\text{MSP}} \ge \tau_M$) enforces multi-criteria filtering, suppressing offline UFAR to 16.07% in Cohort A and 9.54% in Cohort C. However, because both constituent gates operate on downstream functions of the same MobileNetV2 logit activations, the cascade remains fundamentally bounded by the backbone's visual representation.
4. **Proxy Properties:** Continuous ranking analysis for the Dual-Gate evaluates the Energy–MSP linear-margin proxy (exploratory). As established in Section 4.4.2, this proxy correlates strongly with raw Energy scores (Spearman rank correlation $\rho > 0.992$ across all 13,465 evaluated image records), reflecting its mathematical domination by Energy variance ($\sigma \approx 2.15$ vs. $\sigma \approx 0.18$).

---

## 6.5. Prospective Pathways for Multi-Modal Sensing in Post-Harvest Quality Assessment

To address the visual limitations identified in this benchmark, prospective agricultural inspection architectures should explore integrating RGB computer vision with complementary sensing modalities as promising research directions:
1. **Hyperspectral and Near-Infrared Spectroscopy:** Prospective integration of spectroscopy in the near-infrared and short-wave infrared ranges could probe internal fruit quality parameters such as moisture content, sugar concentration, and cellular breakdown, offering non-destructive assessment capabilities that extend beyond exterior RGB surface photography.
2. **Volatile Organic Compound (VOC) and Chemical Sensing:** As a prospective investigation area, specialized gas-sensor arrays and chemical sensing architectures can monitor ambient headspace for volatile markers associated with ripening, decay, or chemical adulteration, providing an orthogonal signal to optical classification [32].
3. **Dynamic Cold-Chain Telemetry Integration:** Future routing decision frameworks could investigate integrating image-based surface assessments with historical transit telemetry (temperature, relative humidity, and transit duration) to support predictive quality management throughout the cold chain. We emphasize that these multi-modal avenues represent prospective research directions rather than proven capabilities of the current offline vision benchmark.
