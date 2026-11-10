# Stage 3.0 Model B V4.1 Inference Compatibility Pilot Report

**Document ID:** `V4_1_INFERENCE_COMPATIBILITY_REPORT.md`  
**Role:** Lead Machine Learning Research Engineer & Scientific Reproducibility Auditor  
**Target Publication:** 5th International Conference on Machine Learning and Data Engineering (ICMLDE 5.0) / *Procedia Computer Science* (Elsevier)  
**Execution Timestamp:** November 10, 2026  
**Evaluation Scope:** Inference Compatibility Pilot on Frozen Primary Checkpoint (Non-destructive; read-only; no model retraining; no test set inspection)

---

## 1. Executive Summary & Final Verdict

This pilot establishes whether the existing frozen Model B V4.1 checkpoint (`MODEL_B_V4_1_CHECKPOINT.keras`) supports the complete suite of open-set recognition (OSR) and out-of-distribution (OOD) scoring mechanisms without requiring retraining, architectural modification, or weight fine-tuning.

Inference was executed across the ground-truth raw validation partition ($N=227$ images, `is_raw == 1`) under strict isolation. All required tensor outputs—raw six-class logits, normalized softmax probabilities, 1,280-dimensional penultimate feature embeddings, top-1 predictions, and maximum softmax confidences—were successfully and deterministically extracted with **0.00e+00 numerical variance** across consecutive runs. The checkpoint file remained 100% byte-identical post-inference.

### **FINAL DECISION: GO**
The frozen Model B V4.1 checkpoint natively and deterministically supports all proposed open-set scoring mechanisms (MSP, Energy-based scoring, ODIN input perturbation, and Ledoit-Wolf regularized Mahalanobis distance) without altering a single trained parameter.

---

## 2. Task 1: Checkpoint Verification & Architecture Audit

### 2.1 Cryptographic & File Verification
- **Target File Path:** `MODEL_B_V4_1_CHECKPOINT.keras`
- **Physical File Size:** Exactly **9,715,984 bytes**
- **Pre-Inference SHA-256:**
  `4a12f354a4157d2b04ed9606df7112c663fe000d924c5264b5f2fa1b3932b6b4`
- **Authoritative Hash Match:** **100% Match** with `MODEL_B_V4_1_CHECKPOINT_SHA256.txt` and `tests/test_reproducibility_v4_1.py`.

### 2.2 Model Architecture & Penultimate Layer Topology
The checkpoint was loaded into memory via `tf.keras.models.load_model(..., compile=False)`. Inspection confirms the model topology:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        MODEL B V4.1 ARCHITECTURAL TOPOLOGY                             │
├───────┬──────────────────────┬────────────────────────┬────────────────────────────────┤
│ Index │ Layer Name           │ Layer Type             │ Tensor Shape (Input -> Output) │
├───────┼──────────────────────┼────────────────────────┼────────────────────────────────┤
│ 0     │ input_tensor         │ InputLayer             │ (None, 224, 224, 3)            │
│ 1     │ mobilenetv2_1.00_224 │ Functional (Backbone)  │ (None, 224, 224, 3) ->         │
│       │                      │                        │ (None, 1280)                   │
│ 2     │ top_dropout          │ Dropout (rate = 0.30)  │ (None, 1280) -> (None, 1280)   │
│ 3     │ predictions          │ Dense (activation=smax)│ (None, 1280) -> (None, 6)      │
└───────┴──────────────────────┴────────────────────────┴────────────────────────────────┘
```

- **Input Dimensions:** `(None, 224, 224, 3)` (RGB imagery, 224 $\times$ 224 pixels).
- **Penultimate Feature Layer:** `top_dropout` (or equivalently the pooling output of `mobilenetv2_1.00_224`). At test time (`training=False`), dropout acts as an identity operator, yielding an exact penultimate representation vector $h(x) \in \mathbb{R}^{1280}$.
- **Classification Head:** Dense layer `predictions` with weights $W \in \mathbb{R}^{1280 \times 6}$ and bias $b \in \mathbb{R}^6$.
- **Class-to-Index Canonical Mapping:**
  ```python
  0: "fresh_apple"
  1: "fresh_banana"
  2: "fresh_orange"
  3: "rotten_apple"
  4: "rotten_banana"
  5: "rotten_orange"
  ```
- **Image Preprocessing:** Strict MobileNetV2 preprocessing:
  $$x_{\text{norm}} = \frac{x}{127.5} - 1.0 \in [-1.0, 1.0]^3$$
  applied to decoded RGB images resized to $224 \times 224$.

---

## 3. Task 2: Raw Validation Input Census

A strict filter was applied to [`FINAL_GROUP_VAL_V4_1.csv`](file:///Users/abby/Desktop/spoilage-predictor/FINAL_GROUP_VAL_V4_1.csv):
```python
df_val_raw = df_val_all[df_val_all["is_raw"] == 1].copy().reset_index(drop=True)
```

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        RAW VALIDATION CENSUS (is_raw == 1)                             │
├─────────────────┬──────────────────────┬──────────────────────┬────────────────────────┤
│ Class Name      │ Manifest Raw Count   │ Verified on Disk     │ Proportion (%)         │
├─────────────────┼──────────────────────┼──────────────────────┼────────────────────────┤
│ rotten_apple    │ 49                   │ 49                   │ 21.59%                 │
│ rotten_banana   │ 46                   │ 46                   │ 20.26%                 │
│ fresh_apple     │ 35                   │ 35                   │ 15.42%                 │
│ fresh_banana    │ 33                   │ 33                   │ 14.54%                 │
│ rotten_orange   │ 33                   │ 33                   │ 14.54%                 │
│ fresh_orange    │ 31                   │ 31                   │ 13.66%                 │
├─────────────────┼──────────────────────┼──────────────────────┼────────────────────────┤
│ TOTAL           │ 227                  │ 227                  │ 100.00%                │
└─────────────────┴──────────────────────┴──────────────────────┴────────────────────────┘
```

- **Validation Row Count:** Exactly **227** images.
- **Augmentation Contamination:** Exactly **0** offline augmented variants (`is_raw == 0`) entered the inference pipeline.
- **Physical File Existence:** Exactly **227 / 227** images confirmed present and readable on physical disk.
- **Concordance:** Exactly matches the empirical distribution documented in [`STAGE2_FINAL_CORRECTION_LOG.md`](file:///Users/abby/Desktop/spoilage-predictor/STAGE2_FINAL_CORRECTION_LOG.md).

---

## 4. Task 3: Output Tensor Extraction & Numerical Verification

An in-memory feature-extraction submodel was constructed non-destructively:
```python
feat_model = tf.keras.Model(inputs=model.inputs, outputs=dense_layer.input)
```
For each batch, outputs were computed via:
$$h(x) = \text{feat\_model}(x, \text{training}=\text{False}) \in \mathbb{R}^{B \times 1280}$$
$$z(x) = h(x) W + b \in \mathbb{R}^{B \times 6}$$
$$p(x) = \text{softmax}(z(x)) \in [0, 1]^{B \times 6}$$

### 4.1 Tensor Shape and Health Verification
```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                         EXTRACTED TENSOR SPECIFICATIONS                                │
├──────────────────────────┬──────────────────┬──────────────┬─────────────┬─────────────┤
│ Output Tensor            │ Shape            │ Data Type    │ NaN Count   │ Inf Count   │
├──────────────────────────┼──────────────────┼──────────────┼─────────────┼─────────────┤
│ Penultimate Features     │ (227, 1280)      │ float32      │ 0           │ 0           │
│ Pre-Softmax Logits       │ (227, 6)         │ float32      │ 0           │ 0           │
│ Softmax Probabilities    │ (227, 6)         │ float32      │ 0           │ 0           │
│ Top-1 Predicted Classes  │ (227,)           │ int64        │ 0           │ 0           │
│ Top-1 Confidences (MSP)  │ (227,)           │ float32      │ 0           │ 0           │
└──────────────────────────┴──────────────────┴──────────────┴─────────────┴─────────────┘
```

- **Probability Summation Axiom:** $\max_i |\sum_{k=1}^6 p_{ik} - 1.0| = 1.79 \times 10^{-7}$ (exact within standard single-precision IEEE 754 floating-point epsilon).
- **Closed-Set Validation Performance:**
  - Raw validation accuracy: **96.92%** ($220 / 227$ correct).
  - Minimum confidence: $0.4225$.
  - Mean confidence: $0.9226$.
  - Maximum confidence: $0.9998$.

---

## 5. Task 4: Repeated Inference Consistency & Determinism

Inference was executed across the identical 227 images in two independent sequential passes (Pass 1 and Pass 2) using fresh dataset iterators:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                         PASS 1 vs. PASS 2 REPRODUCIBILITY                              │
├──────────────────────────────────────────┬──────────────────────┬──────────────────────┤
│ Metric                                   │ Observed Difference  │ Tolerance Threshold  │
├──────────────────────────────────────────┼──────────────────────┼──────────────────────┤
│ Maximum Absolute Feature Difference      │ 0.00e+00             │ < 1.00e-05           │
│ Maximum Absolute Logit Difference        │ 0.00e+00             │ < 1.00e-05           │
│ Maximum Absolute Probability Difference  │ 0.00e+00             │ < 1.00e-05           │
│ Top-1 Prediction Agreement               │ 100.00% (227 / 227)  │ Exactly 100.00%      │
│ Number of Divergent Predictions          │ 0                    │ 0                    │
└──────────────────────────────────────────┴──────────────────────┴──────────────────────┘
```

**Finding:** The inference pipeline on the Apple M4 Metal GPU backend produces bit-for-bit identical results ($0.00\text{e}+00$ deviation) across repeated passes. No nondeterministic dropout, batch normalization updates, or stochastic ops occur during evaluation.

---

## 6. Task 5: Model Integrity Post-Inference

To guarantee that in-memory model wrapping and extraction did not alter weights or serialize changes to disk, the SHA-256 of `MODEL_B_V4_1_CHECKPOINT.keras` was recomputed immediately following inference:

- **Pre-Inference SHA-256:**  `4a12f354a4157d2b04ed9606df7112c663fe000d924c5264b5f2fa1b3932b6b4`
- **Post-Inference SHA-256:** `4a12f354a4157d2b04ed9606df7112c663fe000d924c5264b5f2fa1b3932b6b4`
- **Status:** **100% Byte-Identical and Preserved.**

---

## 7. Task 6: Algorithmic Implementation Feasibility

With the confirmed extraction of $(227, 1280)$ penultimate features and $(227, 6)$ raw logits, all proposed OSR and OOD baseline detectors can be implemented directly without retraining:

### 1. Maximum Softmax Probability (MSP; Hendrycks & Gimpel, 2017)
- **Mathematical Form:** $S_{\text{MSP}}(x) = \max_{k \in \{1,\dots,6\}} p_k(x)$
- **Feasibility:** Trivial numpy operation `np.max(probs, axis=1)`. Natively supported.

### 2. Energy-Based OOD Detection (Liu et al., 2020)
- **Mathematical Form:** $E(x; T) = -T \cdot \log \sum_{k=1}^6 \exp(z_k(x) / T)$
- **Feasibility:** Direct numerical evaluation via `scipy.special.logsumexp(logits / T, axis=1)`. Bypasses softmax normalization hazards. Natively supported.

### 3. ODIN (Liang et al., 2018)
- **Mathematical Form:** Temperature scaling coupled with input gradient perturbations:
  $$\widetilde{x} = x - \epsilon \cdot \text{sign}\left(-\nabla_x \log \frac{\exp(z_{\hat{y}}(x)/T)}{\sum_j \exp(z_j(x)/T)}\right)$$
- **Feasibility:** Because the frozen checkpoint is fully loaded in Keras/TensorFlow, input gradients $\nabla_x$ are directly computable via `tf.GradientTape()` without altering checkpoint weights. Natively supported.

### 4. Ledoit-Wolf Regularized Mahalanobis Distance (Lee et al., 2018)
- **Mathematical Form:** 
  $$M(x) = \min_{k \in \{1,\dots,6\}} (h(x) - \mu_k)^T \mathbf{\Sigma}_{\text{LW}}^{-1} (h(x) - \mu_k)$$
- **Feasibility:** Feature vectors $h(x) \in \mathbb{R}^{1280}$ are cleanly extracted. Using `sklearn.covariance.LedoitWolf`, the empirical covariance matrix $\mathbf{S} \in \mathbb{R}^{1280 \times 1280}$ computed on training features ($N_{\text{train}}=1057$) is analytically shrunk to full rank, guaranteeing a positive-definite, invertible matrix $\mathbf{\Sigma}_{\text{LW}}$. Natively supported.

### 5. Calibrated Selective Prediction (Gate 2)
- **Mathematical Form:** Post-hoc scalar temperature scaling $z / T$ fitted via NLL optimization on validation logits ($N=227$).
- **Feasibility:** Logits and labels are fully serialized; scalar temperature $T$ optimizes rapidly via L-BFGS-B in `< 0.1` seconds. Natively supported.

---

## 8. Summary Audit Table

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        INFERENCE PILOT SPECIFICATION SUMMARY                           │
├─────────────────────────────────────────┬──────────────────────────────────────────────┤
│ Attribute                               │ Verified Value                               │
├─────────────────────────────────────────┼──────────────────────────────────────────────┤
│ Checkpoint SHA-256                      │ 4a12f354a4157d2b04ed9606df7112c663fe000...   │
│ Checkpoint Size                         │ 9,715,984 bytes                              │
│ Image Resolution & Channels             │ 224 x 224 x 3                                │
│ Preprocessing Scaling                   │ [-1.0, 1.0] (mobilenet_v2.preprocess_input)  │
│ Penultimate Feature Dimension           │ Exactly 1,280                                │
│ Output Classification Dimension         │ Exactly 6 classes                            │
│ Raw Validation Sample Size (is_raw==1)  │ Exactly 227 original images                  │
│ Offline Augmented Contamination         │ Exactly 0 variants                           │
│ Pass 1 vs. Pass 2 Logit Difference      │ 0.00e+00                                     │
│ Checkpoint Post-Inference State         │ Byte-identical (Unmutated)                   │
│ External Test Sets Inspected            │ None (0 samples inspected; strictly sealed)  │
│ Retraining Required                     │ None (100% frozen inference)                 │
└─────────────────────────────────────────┴──────────────────────────────────────────────┘
```

---
*Report Certified by Lead ML Research Engineer and Reproducibility Auditor.*

