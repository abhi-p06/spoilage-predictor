# AgriRoute Repository Inventory & Asset Traceability Audit

> **Audit Date:** 2026-11-08  
> **Auditor:** Independent Research Auditor (AgriRoute Research Revision)  
> **Workspace Root:** `/Users/abby/Desktop/spoilage-predictor`  
> **External Manuscript Location:** `/Users/abby/Downloads/main.tex`, `/Users/abby/Downloads/researchpaper-2.docx`  
> **Git Head Commit:** `455b129` (docs: add README, LICENSE, CONTRIBUTING, CI workflow, issue & PR templates)

---

## 1. Executive Summary of Workspace Assets

The workspace contains an end-to-end prototype web application (Flask + MobileNetV2 + BiLSTM + XGBoost) and supporting training scripts, but **critically lacks the trained model weights and raw datasets in the current working tree**. 

In git commit `568fd604b6b6cbd12b4d77e7915afad3b0d437e3` (Sat Aug 15 18:44:11 2026), the author deliberately deleted:
1. `models/cnn_freshness.keras` (25.8 MB)
2. `models/lstm_spoilage.keras` (3.8 MB)
3. `data/sensors/sensor_logs.csv` (4,001 lines)
4. `logs/cnn_training.log` (156 lines)
5. `notebooks/01_cnn_training.ipynb` (885 lines)

Consequently, the web app running on `HEAD` operates entirely via **hardcoded heuristic fallbacks**. Furthermore, the main IEEEtran manuscript (`main.tex`) resides outside the project root in `~/Downloads/main.tex` and contains significant conceptual discrepancies when compared against the codebase.

---

## 2. Complete Workspace File Inventory

| Path | Size (Bytes) | Lines | File Type | Timestamp (UTC/Local) | Role / Category | Verification Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `README.md` | 9,472 | 231 | Markdown | 2026-08-15 / 2026-11-08 | Project Documentation | Present (claims AUC=1.000, 97.22%) |
| `LICENSE` | 1,065 | 21 | Plain Text | 2026-08-15 / 2026-11-08 | Licensing (MIT) | Present |
| `CONTRIBUTING.md` | 2,196 | 82 | Markdown | 2026-08-15 / 2026-11-08 | Guidelines | Present |
| `requirements.txt` | 922 | 42 | Config/Env | 2026-08-15 / 2026-11-08 | Python Dependencies | Present (TF, XGBoost, Flask) |
| `.env.example` | 1,497 | 25 | Config/Env | 2026-08-15 / 2026-11-08 | Environment Template | Present |
| `.gitignore` | 423 | 41 | Git Config | 2026-06-25 / 2026-11-08 | Ignores `models/`, `data/images/` | Present |
| `.github/workflows/ci.yml` | 2,284 | 71 | YAML | 2026-08-15 / 2026-11-08 | GitHub Actions CI | Present (lint + syntax check) |
| `.github/PULL_REQUEST_TEMPLATE.md` | 647 | 26 | Markdown | 2026-08-15 / 2026-11-08 | GitHub Template | Present |
| `.github/ISSUE_TEMPLATE/bug_report.md` | 848 | 36 | Markdown | 2026-08-15 / 2026-11-08 | GitHub Template | Present |
| `.github/ISSUE_TEMPLATE/feature_request.md` | 557 | 23 | Markdown | 2026-08-15 / 2026-11-08 | GitHub Template | Present |
| `download_dataset.py` | 3,386 | 102 | Python | 2026-06-25 / 2026-11-08 | Kaggle Dataset Downloader | Present |
| `generate_sensor_data.py` | 6,274 | 179 | Python | 2026-06-25 / 2026-11-08 | Synthetic Sensor Data Gen | Present (source of BiLSTM leak) |
| `train_all.py` | 19,633 | 482 | Python | 2026-06-25 / 2026-11-08 | Pipeline Runner (all 3 models) | Present (mismatched file extensions) |
| `app/app.py` | 11,849 | 336 | Python | 2026-08-15 / 2026-11-08 | Flask Application Server | Present |
| `app/predict.py` | 13,874 | 381 | Python | 2026-08-15 / 2026-11-08 | Inference Pipeline + Fallbacks | Present |
| `app/mandi_prices.py` | 8,837 | 250 | Python | 2026-08-15 / 2026-11-08 | AGMARKNET API client | Present (contains MD5 fallback) |
| `app/sms_alerts.py` | 4,772 | 138 | Python | 2026-08-15 / 2026-11-08 | Twilio SMS Alert Client | Present |
| `app/templates/index.html` | 28,142 | 741 | HTML/Jinja | 2026-08-15 / 2026-11-08 | Web UI (Input Form + Leaflet) | Present |
| `app/templates/result.html` | 17,998 | 441 | HTML/Jinja | 2026-08-15 / 2026-11-08 | Web UI (Dashboard) | Present |
| `app/static/style.css` | 16,842 | 744 | CSS | 2026-08-15 / 2026-11-08 | Styling | Present |
| `data/sensors/sample_input.csv` | 668 | 25 | CSV | 2026-06-25 / 2026-11-08 | Sample 24h Sequence (Apple) | Present |
| `data/sensors/sensor_logs.csv` | 0 | 0 | CSV | Deleted in `568fd60` | Full Synthetic Sensor Logs | Missing from disk (recoverable from git) |
| `data/images/` | 0 | 0 | Directory | Gitignored | Kaggle Fruit Images | Missing from disk |
| `models/` | 0 | 0 | Directory | Deleted in `568fd60` | Model Checkpoints Directory | Missing entirely from disk |
| `models/cnn_freshness.keras` | 0 | 0 | Keras HDF5/Zip | Deleted in `568fd60` | MobileNetV2 Weights | Missing from disk (recoverable from git `0af3146`) |
| `models/lstm_spoilage.keras` | 0 | 0 | Keras HDF5/Zip | Deleted in `568fd60` | BiLSTM Weights | Missing from disk (recoverable from git `1850576`) |
| `models/lstm_scaler.pkl` | 0 | 0 | Pickle | Deleted in `568fd60` | Sensor Feature StandardScaler | Missing from disk (recoverable from git `1850576`) |
| `models/fusion_xgb.pkl` | 0 | 0 | Pickle | Never committed | XGBoost Fusion Bundle | Missing from disk & git |
| `logs/lstm_training.log` | 133,262 | 129 | Log Text | 2026-06-26 / 2026-11-08 | BiLSTM Training Run Log | Present (documents Epoch 1 val_auc=1.0) |
| `logs/fusion_training.log` | 2,729 | 76 | Log Text | 2026-06-26 / 2026-11-08 | XGBoost Training Run Log | Present (documents missing CNN model) |
| `logs/cnn_training.log` | 0 | 0 | Log Text | Deleted in `568fd60` | CNN Training Run Log | Missing from disk (recoverable from git `0af3146`) |
| `notebooks/01_cnn_training.py` | 14,846 | 452 | Python | 2026-06-26 / 2026-11-08 | CNN Training Script | Present |
| `notebooks/01_cnn_training.ipynb` | 0 | 0 | Jupyter NB | Deleted in `568fd60` | CNN Training Notebook | Missing from disk (recoverable from git `b2e8678`) |
| `notebooks/02_lstm_training.py` | 10,723 | 286 | Python | 2026-06-26 / 2026-11-08 | BiLSTM Training Script | Present |
| `notebooks/02_lstm_training.ipynb` | 18,342 | 483 | Jupyter NB | 2026-06-25 / 2026-11-08 | BiLSTM Training Notebook | Present |
| `notebooks/03_fusion_training.py` | 13,842 | 383 | Python | 2026-06-26 / 2026-11-08 | Fusion Training Script | Present |
| `notebooks/03_fusion_training.ipynb` | 24,192 | 609 | Jupyter NB | 2026-06-25 / 2026-11-08 | Fusion Training Notebook | Present |
| `notebooks/README_notebooks.py` | 742 | 21 | Python | 2026-06-25 / 2026-11-08 | Notebook Index Doc | Present |
| `notebooks/cnn_training_curves.png` | 96,964 | Binary | PNG Image | 2026-06-26 / 2026-11-08 | MobileNetV2 Loss/Acc Curves | Present |
| `notebooks/sample_batch.png` | 13,590 | Binary | PNG Image | 2026-06-26 / 2026-11-08 | Kaggle Sample Augmentations | Present |
| `notebooks/lstm_training_curves.png` | 66,989 | Binary | PNG Image | 2026-06-26 / 2026-11-08 | BiLSTM Loss/AUC Curves | Present |
| `notebooks/lstm_evaluation.png` | 61,790 | Binary | PNG Image | 2026-06-26 / 2026-11-08 | BiLSTM ROC & Conf Matrix | Present |
| `notebooks/lstm_ethylene_eda.png` | 141,050 | Binary | PNG Image | 2026-06-26 / 2026-11-08 | Ethylene Trajectory Plot | Present |
| `notebooks/fusion_days_scatter.png` | 53,014 | Binary | PNG Image | 2026-06-26 / 2026-11-08 | Days-to-spoilage Reg Plot | Present |
| `notebooks/fusion_evaluation.png` | 75,070 | Binary | PNG Image | 2026-06-26 / 2026-11-08 | Fusion ROC & Conf Matrix | Present |
| `notebooks/fusion_feature_dist.png` | 55,839 | Binary | PNG Image | 2026-06-26 / 2026-11-08 | Feature Distribution Plots | Present |
| `reports/research_brief.md` | 32,848 | 400 | Markdown | 2026-08-04 / 2026-11-08 | Literature Review & Gaps | Present |
| `reports/pitch_preparation.md` | 24,841 | 222 | Markdown | 2026-06-29 / 2026-11-08 | Viva Exam Q&A Guide | Present (honest about synthetic data) |

---

## 3. External Manuscript Inventory

The paper manuscript files are located outside the project root:

1. **`~/Downloads/main.tex`** (38,320 bytes, 369 lines, last modified Aug 11 19:12):
   - IEEEtran conference LaTeX paper: *"AgriRoute: A Vision-Based Post-Harvest Risk System: Multimodal Spoilage, Transport-Route, and Price-Risk Prediction for Smallholder Produce Sellers"*.
   - Contains 10 sections, 27 references, 4 placeholder figures, and multiple references to an undefined "Table V".
2. **`~/Downloads/researchpaper-2.docx`** (40,218 bytes, last modified Aug 12 00:44):
   - Microsoft Word source draft from which `main.tex` was converted.
3. **`~/Downloads/researchpaper-2.pdf`** (172,964 bytes, last modified Aug 12 11:53):
   - Rendered PDF version of the Word draft.

---

## 4. Manuscript Placeholders, Incomplete Notes & Unfinished Text

An exhaustive forensic scan of `~/Downloads/main.tex` reveals multiple severe placeholders, unverified claims, and editorial relics:

1. **Editorial Preamble Block (Lines 6–42):**
   - Explicit instructions left in file: `NOTES TO THE AUTHOR -- read before submitting, then delete this block.`
   - Mentions section renumbering, missing figures, missing Table V, and uncited references.
2. **Author Identity Placeholders (Lines 57, 61):**
   - Line 57: `\IEEEauthorblockN{Esh {[}Surname---to confirm{]}\textsuperscript{*}}`
   - Line 61: `{[}email---to confirm{]}@somaiya.edu`
   - Reviewer 2 specifically flagged: *"Remove all incomplete author-role or drafting notes, including 'Specific roles can be updated before submission'"*.
3. **Missing "Table V" Phantom References:**
   - Referenced in text at:
     - Line 26: `Table V. Referenced repeatedly (accuracy figures, alpha/beta/w1/w2 values, dataset composition) but never defined in the supplied draft.`
     - Line 94: `...are reported in Section VI once finalised (see Table V).`
     - Line 145: `...exact backbone, training-set composition, and measured accuracy are to be finalised in Section VI-A / Table V.`
     - Line 193: `The exact composition of the dataset behind the CNN's training ... is left to Table V rather than stated here...`
     - Line 209: `The fitted values of \alpha and \beta are scoring-function implementation details, reported once confirmed in Table V...`
     - Line 218: `The exact values of w1, w2, and that calibration curve remain implementation details pending confirmation in Table V...`
   - **Finding:** Table V does not exist anywhere in the manuscript, nor do the parameters $\alpha, \beta, w_1, w_2$ exist in code.
4. **Empty Placeholder Figures:**
   - Fig. 1 (`fig:architecture`): Empty box `\fbox{\rule{0pt}{2.4cm}\rule{0.85\linewidth}{0pt}}`
   - Fig. 2 (`fig:route-selection`): Empty box `\fbox{\rule{0pt}{2.2cm}\rule{0.85\linewidth}{0pt}}`
   - Fig. 3 (`fig:risk-breakdown`): Empty box `\fbox{\rule{0pt}{2.2cm}\rule{0.85\linewidth}{0pt}}`
   - Fig. 4 (`fig:price-trend`): Empty box `\fbox{\rule{0pt}{2.2cm}\rule{0.85\linewidth}{0pt}}`
5. **Uncited Bibliography Items:**
   - References `\bibitem{ref19}` through `\bibitem{ref27}` (Nagpal et al., Darwish et al., Gnassounou et al., Ouyang et al., Chen et al., Wang et al., Lee et al., Ganin & Lempitsky, Sun & Saenko) appear in `\begin{thebibliography}` but are **never cited in the body text** (only `\cite{ref1}` through `\cite{ref18}` appear in body text).
6. **Internal Report Citations:**
   - Reference `\bibitem{ref18}` cites *"Post-harvest spoilage predictor for small farmers in India," unpublished undergraduate project report, Dept. of Artificial Intelligence and Data Science, K. J. Somaiya College of Engineering, Mumbai, India, 2025--2026.*
   - Used repeatedly in text to justify physics-constrained models and pilot data that are not publicly retrievable or verifiable.

