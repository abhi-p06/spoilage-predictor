# Strategic Research Recommendations for Paper Revision

> **Audit Date:** 2026-11-09  
> **Auditor:** Independent Scientific Auditor  
> **Document:** `research_audit/08_RESEARCH_RECOMMENDATIONS.md`  
> **Scope:** Concrete scientific, methodological, architectural, and editorial actions to convert the manuscript into a rigorous, publishable submission for ICMLDE 5.0.

---

## 1. Executive Strategy: "Rigor & Transparency Over Inflated Claims"

The fundamental vulnerability identified in the original manuscript is a misalignment between **what the software prototype actually is** and **what the manuscript claimed it to be**. Rather than defending indefensible artifacts (such as an artificial AUC of 1.000 or phantom routing equations), the revised paper will adopt a posture of absolute scientific transparency:

1. **Retract synthetic artifacts openly:** Acknowledge synthetic data leakage directly and replace trivial sequence classification with realistic noisy simulation or clear framework positioning.
2. **Reconcile math with reality:** Strip out non-existent equations ($G, S$) and phantom Table V references; present the actual XGBoost stacking architecture and fallback heuristics honestly.
3. **Elevate empirical rigor where feasible:** Provide multi-backbone vision benchmarking (MobileNetV2 vs. EfficientNetB0 vs. ResNet50) with 95% bootstrap confidence intervals, calibration analysis (ECE), and out-of-distribution evaluation.
4. **De-claim operational readiness:** Acknowledge $N=0$ physical fleet trials and present a prospective multi-shipment field trial protocol to satisfy Reviewer 3.

---

## 2. Pillar-by-Pillar Action Plan

### Pillar 1: Time-Series & Sensor Model (Resolving REV1-03)
- **Action 1.1:** Retract the claim that the BiLSTM achieved a valid empirical AUC of 1.000.
- **Action 1.2:** In Section IV-D and Section VI-D, explicitly state:
  > *"Initial sequence models trained on linearly separable synthetic sensor distributions exhibited trivial saturation ($\text{AUC} = 1.000$), an artifact of non-overlapping generator thresholds. In this revised evaluation, we introduce stochastic biological decay kinetics with overlapping variance, yielding realistic classification performance..."*
- **Action 1.3:** Alternatively, retain the BiLSTM strictly as a **"Designed Physics-Constrained Extension"** (as already outlined in Section IV-D and Table II), emphasizing that empirical validation is reserved for physical sensor deployment.

### Pillar 2: Computer Vision & Multi-Backbone Benchmark (Resolving REV1-02, REV1-04, REV2-03)
- **Action 2.1:** Fix the Keras 3 evaluation script bug (`KeyError: 'accuracy'`) in `notebooks/01_cnn_training.py`.
- **Action 2.2:** Establish a clean, leak-free 70/15/15 train/val/test split audited with perceptual hashing (pHash) to prevent near-duplicate leakage.
- **Action 2.3:** Implement, train, and benchmark three backbones under unified conditions:
  - **MobileNetV2** (lightweight edge baseline).
  - **EfficientNetB0** (compound-scaled modern baseline).
  - **ResNet50** (deep residual benchmark).
- **Action 2.4:** Compute 95% non-parametric bootstrap confidence intervals ($B = 1,000$) for Accuracy, Macro Precision, Macro Recall, Macro F1, and Macro AUC.
- **Action 2.5:** Perform zero-shot out-of-distribution (OOD) evaluation on an external public dataset (e.g. Fruits-360 or real-market produce) to quantify domain transfer degradation.
- **Action 2.6:** Generate Grad-CAM heatmaps for true positive and false negative cohorts to confirm attention localizes to physical spoilage lesions rather than background artifacts.
- **Action 2.7:** Clarify produce scope: explicitly state that the visual classifier operates on Apple, Banana, and Orange, with Tomato and Mango classified as planned expansions.

### Pillar 3: Mathematical Model & Fusion Architecture (Resolving REV1-01, REV2-01)
- **Action 3.1:** Eliminate Equations (2) and (3) ($G = \text{clip}(\alpha \tau D - \beta c)$, $S = w_1 V + w_2 G$) and all 6 references to non-existent "Table V".
- **Action 3.2:** Formalize the actual deployed multi-modal architecture:
  - Multi-modal feature vector: $\mathbf{x} = [f_{\mathrm{CNN}}, f_{\mathrm{sensor}}, d, c, p]^T$.
  - XGBoost stacking classifier for spoilage probability: $P(\text{spoilage}) = \operatorname{XGB}_{\mathrm{clf}}(\mathbf{x})$.
  - XGBoost regressor for shelf-life estimation: $\hat{T}_{\mathrm{days}} = \operatorname{XGB}_{\mathrm{reg}}(\mathbf{x})$.
  - Operational fallback equation used when models are offline.
- **Action 3.3:** Document decision thresholds explicitly:
  - Green (Safe): $P < 0.35$
  - Yellow (Moderate Risk): $0.35 \le P < 0.70$
  - Red (High Spoilage Risk): $P \ge 0.70$
- **Action 3.4:** Execute an ablation sensitivity analysis sweeping fusion weight parameter $\alpha \in [0.0, 1.0]$ to provide the mathematical justification demanded by Reviewer 2.

### Pillar 4: Probability Calibration & Uncertainty (Resolving REV1-03)
- **Action 4.1:** Compute the Expected Calibration Error (ECE) and Brier Score on validation predictions.
- **Action 4.2:** Apply post-hoc Temperature Scaling to convert overconfident neural network logits into well-calibrated probabilities suitable for downstream risk alerting.
- **Action 4.3:** Include a Reliability Diagram (empirical accuracy vs. mean confidence across 10 bins) demonstrating ECE reduction.

### Pillar 5: Transport Routing & Field Reality (Resolving REV1-05, REV3-01, REV3-02)
- **Action 5.1:** Disclose $N=0$ physical fleet shipments prominently in the Abstract, Introduction, and Limitations sections.
- **Action 5.2:** Re-label the Guntur $\to$ Rajkot case study as an **"Illustrative Software Execution Demonstration"**.
- **Action 5.3:** Acknowledge that the current web app visualizes driving routes via client-side OSRM as an informational display for the driver, rather than claiming a dynamic vehicle routing optimization algorithm.
- **Action 5.4:** Detail a prospective 4-phase field evaluation protocol:
  - Phase 1: In-situ image acquisition across rural mandis ($N = 2,000$ images).
  - Phase 2: Benchtop sensor rig validation with destructive quality testing (Brix, penetrometer firmness).
  - Phase 3: Paired transit trial ($N = 20$ vehicle shipments across 3 inter-state routes).
  - Phase 4: Statistical outcome evaluation (economic loss reduction vs. standard transport).

### Pillar 6: Competitive Literature & Platform Benchmarking (Resolving REV1-04, REV3-03)
- **Action 6.1:** Insert a 6-row State-of-the-Art Literature Comparison Table in Section II comparing AgriRoute with recent (2022–2026) published post-harvest systems across sensing modalities, perishability kinetics, and routing coupling.
- **Action 6.2:** Insert an Agri-Logistics Commercial Platform Comparison Table in Section III benchmarking AgriRoute against AgNext, Intello Labs, CropIn, Ecozen Eco-Frost, and Stellapps.

### Pillar 7: Editorial & Submission Hygiene (Resolving REV2-02)
- **Action 7.1:** Delete the author memo block (lines 6–46 of `main.tex`).
- **Action 7.2:** Confirm author name, affiliation, and Somaiya University email address.
- **Action 7.3:** Verify all citations against verified Crossref/OpenAlex DOIs; eliminate dummy references.
- **Action 7.4:** Ensure all referenced tables and figures exist, are numbered sequentially, and are accompanied by complete, non-empty captions.

