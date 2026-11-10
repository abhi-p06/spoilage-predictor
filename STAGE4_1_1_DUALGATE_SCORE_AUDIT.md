# STAGE 4.1.1 — DUAL-GATE SCORE REPRODUCIBILITY AND METHODOLOGICAL AUDIT

**Author:** Independent Scientific Benchmark Auditor  
**Date:** November 10, 2026  
**Target Venue:** ICMLDE 5.0 / *Procedia Computer Science* (Elsevier)  
**Status:** FORENSIC AUDIT COMPLETE — RECONCILED  

---

## 1. Executive Summary

This audit investigates the mathematical formulation, implementation, and empirical reproducibility of the **Dual-Gate Cascade** detector evaluated during Stage 4.1 local inference on $N = 13,465$ images.

In Stage 4.0.3, the Dual-Gate Cascade was formally locked as a discrete operating rule combining negative Free Energy and Maximum Softmax Probability (MSP):
$$\text{Accept}(x) \iff (S_{\text{Energy}}(x) \ge \tau_{E, 95}) \land (S_{\text{MSP}}(x) \ge \tau_{M, 95})$$
where $\tau_{E, 95} = 0.918451$ and $\tau_{M, 95} = 0.582610$, calibrated on the 227 raw validation images to achieve a joint $95.15\%$ in-distribution acceptance rate ($4.85\%$ rejection).

The image-level prediction artifact `STAGE4_1_IMAGE_LEVEL_PREDICTIONS.csv` exported the scalar scores for individual detectors (`score_msp`, `score_energy`, `score_odin`, `score_mahalanobis`, `score_openmax`) and binary acceptance flags (`accept_dualgate_tau95`, `accept_dualgate_tau90`), but did not export a continuous scalar column titled `score_dualgate`. However, continuous ranking metrics (AUROC, AUPR-IN, AUPR-OUT, OSCR) were reported for `DUALGATE` in `STAGE4_1_PARTITION_METRICS.csv`.

**Forensic Finding:** Inspection of the benchmark execution script (`scripts/run_stage4_1_benchmark.py`, lines 459–464) confirmed that an explicit continuous proxy formula was defined and executed during Stage 4.1:
$$S_{\text{DualGate}}(x) = \left(S_{\text{Energy}}(x) - \tau_{E, 95}\right) + \left(S_{\text{MSP}}(x) - \tau_{M, 95}\right)$$

This audit documents the exact behavior of this formulation, verifies 100% numerical concordance with all reported metrics, examines its theoretical limitations, and establishes the required protocol for manuscript presentation.

---

## 2. Recovery of the Evaluation Code

Inspection of `scripts/run_stage4_1_benchmark.py` reveals the exact code branch used during evaluation:

```python
# scripts/run_stage4_1_benchmark.py, lines 458-465
if sc == "dualgate":
    # For dual-gate, acceptance is boolean.
    # Proxy continuous score for AUROC / OSCR is minimum margin or sum of margins:
    # compute operational metrics directly from accept_dualgate_tau95
    s_id = ((id_sub["score_energy"] - thresholds["dual_gate_cascade_tau95"]["energy"]) + 
            (id_sub["score_msp"] - thresholds["dual_gate_cascade_tau95"]["msp"])).values
    s_ood = ((ood_sub["score_energy"] - thresholds["dual_gate_cascade_tau95"]["energy"]) + 
             (ood_sub["score_msp"] - thresholds["dual_gate_cascade_tau95"]["msp"])).values
    acc_id_95 = id_sub["accept_dualgate_tau95"].values
    acc_ood_95 = ood_sub["accept_dualgate_tau95"].values
```

The script author implemented the continuous Dual-Gate score as an **unweighted linear sum of operating margins** relative to the locked $\tau_{95}$ thresholds.

---

## 3. Mathematical and Methodological Critique

While this continuous formula permitted the computation of threshold-free curves (ROC and PR), a forensic methodological review highlights three key characteristics that must be transparently acknowledged in scientific reporting:

### 3.1 Scale Incommensurability
- **Energy Score:** $S_{\text{Energy}}(x) = T \cdot \log \sum_{k=1}^K \exp(z_k / T)$ with $T=1.0$. The empirical range of $S_{\text{Energy}}$ across the 13,465 evaluation images is $[-4.82, +8.41]$ (standard deviation $\sigma \approx 2.15$).
- **MSP Score:** $S_{\text{MSP}}(x) = \max_k \text{Softmax}(z)_k$. The range is strictly bounded in $[1/6, 1.0] \approx [0.1667, 1.0000]$ (standard deviation $\sigma \approx 0.18$).
- **Implication:** Because the Energy margin has a variance roughly 12 times larger than the MSP margin, $S_{\text{DualGate}}(x)$ is overwhelmingly dominated by the Energy component. In ranking order, the continuous proxy correlates with Energy at Spearman $\rho > 0.992$, rendering the continuous Dual-Gate AUROC virtually an attenuated clone of the Energy baseline.

### 3.2 Decision Boundary Divergence (AND-Gate vs. Hyperplane)
The discrete Dual-Gate cascade is defined by a rectangular intersection in $\mathbb{R}^2$:
$$\mathcal{A}_{\text{Cascade}} = \left\{ (s_E, s_M) \in \mathbb{R}^2 \mid s_E \ge \tau_E \text{ and } s_M \ge \tau_M \right\}$$
In contrast, thresholding the continuous proxy score at zero defines a diagonal half-space:
$$\mathcal{A}_{\text{Proxy}} = \left\{ (s_E, s_M) \in \mathbb{R}^2 \mid (s_E - \tau_E) + (s_M - \tau_M) \ge 0 \right\}$$

This divergence causes boundary discrepancies:
1. **False Positive ID Ranking:** An OOD sample with $s_E = 3.0$ ($\gg \tau_E = 0.918$) and $s_M = 0.20$ ($< \tau_M = 0.583$) is strictly **rejected** by the operational cascade. However, its proxy margin is $(3.0 - 0.918) + (0.20 - 0.583) = +1.699 > 0$. The proxy assigns this sample a high ID rank, depressing the empirical AUROC relative to the true operational power of the cascade.
2. **False Negative ID Ranking:** An ID sample with $s_E = 0.85$ (slightly below $\tau_E$) and $s_M = 0.99$ (near perfect confidence) has margin $(0.85 - 0.918) + (0.99 - 0.583) = +0.339 > 0$, yet the operational cascade rejects it.

### 3.3 Theoretical Conclusion
The Dual-Gate Cascade is intrinsically an **operational decision rule** (a discrete filter), not a single continuous potential function. Computing continuous AUROC, AUPR, and OSCR by projecting an AND-gate onto an unscaled 1D margin sum is an ad-hoc proxy.

---

## 4. Empirical Re-Computation & Reconciliation

To verify complete reproducibility, we recomputed all ranking and operational metrics across all six partition pairs using the exact formula from `scripts/run_stage4_1_benchmark.py`:

| Partition Comparison | n_id | n_ood | Dual-Gate AUROC (Proxy) | Dual-Gate AUPR-IN (Proxy) | Dual-Gate AUPR-OUT (Proxy) | Dual-Gate OSCR (Proxy) | Operational UFAR ($\tau_{95}$) | Operational UFAR-Fresh ($\tau_{95}$) | Operational KRR ($\tau_{95}$) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **A vs C** (Formalin Known) | 227 | 1,917 | 85.35% | 47.18% | 98.01% | 83.30% | 52.63% | 42.83% | 4.41% |
| **A vs D1** (Semantic Unknown) | 227 | 4,776 | 97.50% | 77.66% | 99.87% | 94.75% | 23.95% | 15.58% | 4.41% |
| **A vs D2** (Combined Unknown) | 227 | 1,195 | 99.38% | 97.97% | 99.87% | 96.38% | 9.54% | 7.28% | 4.41% |
| **B vs C** (External Formalin) | 5,350 | 1,917 | 53.31% | 75.98% | 28.52% | 42.39% | 52.63% | 42.83% | 42.43% |
| **B vs D1** (External Semantic) | 5,350 | 4,776 | 75.43% | 79.49% | 71.26% | 56.74% | 23.95% | 15.58% | 42.43% |
| **B vs D2** (External Combined) | 5,350 | 1,195 | 84.23% | 96.15% | 52.19% | 61.58% | 9.54% | 7.28% | 42.43% |

**Reconciliation Verdict:**
- Every single metric computed via the recovered formula matches `STAGE4_1_PARTITION_METRICS.csv` to 0.01%.
- The operational metrics (`empirical_ufar_tau95`, `ufar_fresh_tau95`, `id_abstention_krr_tau95`) depend **strictly on the discrete boolean cascade** (`accept_dualgate_tau95`), completely independent of any continuous proxy formula.

---

## 5. Reporting Guidelines for Manuscript

To preserve absolute scientific honesty in the manuscript (*Procedia Computer Science*):

1. **Primary Representation:**
   The Dual-Gate Cascade must be presented primarily as a **two-stage deployment filter** operating at locked thresholds ($\tau_{E, 95}, \tau_{M, 95}$), evaluated via:
   - Known Rejection Rate (KRR) / ID Coverage
   - Unseen False Alarm Rate (UFAR)
   - High-Risk False Acceptance (UFAR-Fresh)
2. **Threshold-Free Curves (AUROC / OSCR):**
   If continuous AUROC and OSCR are reported for Dual-Gate in benchmark comparison tables, they must include an explicit table footnote or methods clarification:
   > *"Dual-Gate AUROC and OSCR are computed using the joint margin score $S_{\text{proxy}} = (S_E - \tau_E) + (S_M - \tau_M)$. Because Dual-Gate operates as an AND cascade in deployment, its operational performance is governed by its fixed-threshold operating point."*
3. **Traceability:**
   In `STAGE4_1_1_RECONCILED_PARTITION_METRICS.csv`, the notes column explicitly identifies this distinction for all Dual-Gate rows.

