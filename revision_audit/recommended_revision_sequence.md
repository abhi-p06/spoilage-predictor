# Recommended Revision Sequence & Implementation Roadmap

> **Audit Date:** 2026-11-08  
> **Target Venue:** Elsevier Procedia Computer Science / IEEE Conference Revision  
> **Core Objective:** Systematically eliminate all scientific validity risks, achieve 1:1 parity between code and manuscript, and prepare an airtight point-by-point reviewer response.

---

## Phased Revision Roadmap

```
┌─────────────────────────────────────────────────────────────┐
│ Phase 1: Manuscript Sanitization & De-Claiming              │
│ - Remove drafting notes, dummy surnames, phantom Table V    │
│ - De-claim field validation (relabel N=0 demo)              │
│ - Retract BiLSTM AUC=1.000 leakage artifact                 │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Phase 2: Codebase Parity & Checkpoint Restoration           │
│ - Fix Keras 3 evaluation crash in 01_cnn_training.py        │
│ - Align predict.py and main.tex mathematics (1:1 parity)    │
│ - Restore model weights from git history into models/       │
│ - Connect distance_km to inference pipeline                 │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Phase 3: Rigorous Empirical Re-Evaluation                   │
│ - Extract per-class precision, recall, F1, confusion matrix │
│ - Document XGBoost feature importances & ablation study     │
│ - Re-evaluate BiLSTM under realistic noise/overlap          │
│ - Evaluate price trend module on real AGMARKNET historicals │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Phase 4: Literature & Platform Benchmarking                 │
│ - Sourced comparison table vs SOTA agri-logistics platforms │
│ - Verified comparison with recent 2024–2026 literature      │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Phase 5: Prospective Field Protocol & Reviewer Packaging    │
│ - Write complete, publishable multi-shipment field protocol │
│ - Draft point-by-point reviewer response (Reviewers 1–3)   │
│ - Run final paper readiness check                           │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Manuscript Sanitization & De-Claiming (Immediate)

1. **Delete Author Drafting Preamble:**
   - Remove lines 6–42 in `main.tex` (`NOTES TO THE AUTHOR -- read before submitting...`).
2. **Resolve Author Block Placeholders:**
   - Replace `Esh [Surname---to confirm]` (line 57) and `[email---to confirm]@somaiya.edu` (line 61) with verified author details.
3. **Eliminate Phantom "Table V" Citations:**
   - Remove the 6 placeholder references to "Table V" across lines 26, 94, 145, 193, 209, 218.
   - Replace with actual data tables: Table III (Dataset Class Distribution & Performance) and Table IV (XGBoost Feature Weights & Ablation).
4. **De-Claim Field Validation & Retract AUC=1.000:**
   - In Abstract, Section I, and Section VII-A, explicitly state that the Guntur–Rajkot shipment was an **end-to-end software integration test ($N=0$ physical shipments)**.
   - Retract the claim that the BiLSTM achieves AUC=1.000. Transparently explain the synthetic non-overlapping distribution artifact identified during internal audit.
5. **Harmonize Produce Species Scope:**
   - State clearly that the visual classification module was trained and evaluated on **Apple and Banana** (plus Orange), and explicitly identify Tomato and Mango as target extensions undergoing data acquisition.

---

## Phase 2: Codebase Parity & Checkpoint Restoration

1. **Restore Trained Checkpoints:**
   - Recover `models/cnn_freshness.keras`, `models/lstm_spoilage.keras`, and `models/lstm_scaler.pkl` from git commits `0af3146` and `1850576`.
   - Verify that running `python app/predict.py` executes real model inference rather than falling back to random numbers.
2. **Fix Keras 3 Evaluation Crash in `notebooks/01_cnn_training.py`:**
   - Fix line 396: replace `dict(zip(metrics_names, test_results))["accuracy"]` with robust metric key extraction (`val_acc = test_results[1]`).
   - Run complete test set evaluation to generate the final confusion matrix and classification report.
3. **Connect Route Distance to Decision Logic:**
   - In `app/app.py` line 200, pass `distance_km` into `run_prediction()`.
   - In `app/predict.py`, incorporate transit exposure ($D$) into the XGBoost feature vector or risk scoring formula so that route length physically influences the predicted days-to-spoilage.
4. **Standardize Mathematical Formulas Between Code and Manuscript:**
   - Choose between:
     - *Approach A (Match Code to Paper):* Implement $G = \operatorname{clip}(\alpha \tau D - \beta c, 0, 100)$ and $S = w_1 V + w_2 G$ directly in `predict.py` with empirical weights.
     - *Approach B (Match Paper to Code):* Rewrite Section VI-B/VI-C to formally specify the XGBoost multimodal stacking classifier with input vector $\mathbf{x} = [V, R_{\mathrm{sensor}}, D, c, p]^T$.

---

## Phase 3: Rigorous Empirical Re-Evaluation

1. **Vision Model Per-Class Evaluation:**
   - Compute and tabularize:
     - Per-class Precision, Recall, and F1-score for Fresh Apple, Fresh Banana, Rotten Apple, Rotten Banana (and Oranges).
     - Global Accuracy and Macro F1.
     - Confusion matrix figure to replace placeholder Fig. 1.
2. **XGBoost Feature Importance & Ablation Study (Reviewer 2):**
   - Run a formal leave-one-feature-out ablation study on the fusion model:
     - Baseline (Full multimodal: Vision + Sensor + Route + Metadata)
     - Vision-only
     - Sensor-only
     - Vision + Route (without sensors)
   - Tabularize cross-validation ROC-AUC and MAE for each configuration to justify the fusion design.
3. **Sensor Model Audit & Realistic Noise Benchmark (Reviewer 1):**
   - In `generate_sensor_data.py`, generate a realistic benchmark with overlapping gas distributions and Gaussian sensor noise.
   - Evaluate the BiLSTM on this challenging benchmark and report an honest, plausible ROC-AUC (e.g. 0.82–0.88) alongside an explanation of the baseline.
4. **Mandi Price Verification on Real AGMARKNET Series:**
   - Run `app/mandi_prices.py` on real historical AGMARKNET price series for Guntur and Rajkot.
   - Report actual historical price variance and calculate retrospective 3-day forecast RMSE/MAE.

---

## Phase 4: Literature & Platform Benchmarking (Reviewers 1 & 3)

1. **State-of-the-Art Academic Matrix:**
   - Leverage `reports/research_brief.md` to construct a comparative table in Section II benchmarking AgriRoute against 6 recent peer-reviewed systems (2023–2026).
2. **Commercial Platform Comparison Table (Reviewer 3):**
   - Add a comparative table benchmarking AgriRoute against real-world systems:
     - **AgNext Technologies** (Qualix computer vision + spectrophotometry)
     - **Intello Labs** (Intello Track / Intello Sort image-based grading)
     - **CropIn Technology** (CropIn Cloud satellite/weather advisory)
     - **Ecozen Solutions** (Eco-Frost solar cold storage IoT)
   - Compare on: Sensing modalities, per-unit hardware cost, target user (fleet vs smallholder), offline capability, and price integration.

---

## Phase 5: Prospective Field Protocol & Final Packaging

1. **Develop Comprehensive Field Evaluation Protocol (Reviewer 3):**
   - Expand Section VII-B into a formal prospective field trial protocol:
     - **Study Design:** 3 distinct inter-state transit corridors in Maharashtra and Andhra Pradesh.
     - **Sample Size:** 30 shipment batches per corridor, 50 sampled fruit units per batch.
     - **Instrumentation:** Low-cost IoT datalogger (ESP32 + MQ-136 ethylene + Sensirion SHT31 temp/RH) logging at 15-minute intervals.
     - **Ground Truth Assaying:** Pre- and post-transit Brix (refractometer), flesh firmness (penetrometer), and visual spoilage grading.
     - **Statistical Endpoints:** Spoilage risk calibration curves, transit loss reduction %, and Brier score.
2. **Draft Point-by-Point Reviewer Response:**
   - Create `reviewer_response_draft.md` mapping every comment from Reviewers 1–3 to the verified changes, revised equations, new tables, and exact manuscript lines.
3. **Compile and Pagination Check:**
   - Replace all `\fbox` boxes with generated PNG figures (`notebooks/sample_batch.png`, route map screenshot, confusion matrix, price chart).
   - Verify that citations `[19]–[27]` are either cited in body text or removed from bibliography.
   - Compile PDF and run final paper-readiness audit.

