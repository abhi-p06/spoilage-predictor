# Open-Set Fruit Quality Classification: Novelty & Scientific Integrity Audit

**Role:** Principal Investigator & Academic Research Director  
**Target Venues:** 5th International Conference on Machine Learning and Data Engineering (ICMLDE 5.0) / *Procedia Computer Science* (Elsevier)  
**Investigation Date:** November 10, 2026  
**Status:** Strategic Research Audit (Non-destructive; no alterations to V4.1 checkpoints, code, or datasets)

---

## 1. Executive Summary & Research Question Formulation

### 1.1 The Proposed Research Question
> *"Can a risk-aware open-set fruit quality classifier recognize known fresh/rotten fruit conditions while rejecting unfamiliar or potentially unsafe fruit conditions under cross-dataset shift?"*

This research question pivots the AgriRoute project away from an unverified "smart routing application" narrative toward a foundational machine learning and computer vision challenge in agricultural pattern recognition: **Open-Set Recognition (OSR) and Out-of-Distribution (OOD) Abstention under Multi-Source Covariate and Semantic Domain Shift**.

### 1.2 Core Thesis of the Investigation
1. **The Closed-World Illusion in Post-Harvest DL:** Current post-harvest computer vision models (including our own Model A and Model B) operate under the rigid *closed-set assumption* that test samples strictly belong to pre-defined training categories ($K$ known classes). When presented with unseen fruit varieties, novel fungal pathogens, physiological disorders, or chemical preservation adulterations (e.g., formalin dipping), closed-set classifiers invariably produce catastrophic overconfident false predictions—often classifying severely damaged or toxic items as "Fresh".
2. **Has Open-Set Rejection of Formalin-Mixed Fruits Been Demonstrated?** **NO.** A comprehensive review of the peer-reviewed literature confirms that **no existing publication has evaluated the open-set rejection of unseen formalin-treated fruits**. Existing works (such as *FruitVision* and *DurbeenNet*) formulate formalin detection as a standard, closed-set supervised 3-class or 8-class classification task where the model is explicitly trained on labeled formalin-treated images.
3. **The Biophysical Reality & Chemical Warning:** **RGB cameras cannot directly detect formaldehyde ($CH_2O$).** Formaldehyde is a colorless, volatile compound in aqueous solution. Any vision model identifying "formalin-mixed" fruit from standard RGB images is responding to *secondary visual artifacts* (unnatural skin dehydration, delayed enzymatic browning, irregular surface glazes, chemical burns, or camera/lighting artifacts). Claiming RGB-based "chemical verification" is scientifically illegitimate and constitutes pseudoscience.
4. **Legitimate Scientific Framing:** The phenomenon can only be scientifically defended if framed as:
   > **"Detecting uncharacterized visual surface anomalies and preserving-agent physical deviations as Out-of-Distribution (OOD) / Open-Set conditions, thereby abstaining from safety-critical classification, rather than claiming direct optical spectroscopy of chemical toxins."**

---

## 2. Literature Audit: Food Quality, OOD Detection, and Adulteration

### 2.1 The Landscape of Agricultural Open-Set Recognition (OSR)
While OSR has matured in mainstream computer vision following the seminal works of Scheirer et al. (2013), Bendale & Boult (2016), and Vaze et al. (2022), its penetration into post-harvest fruit inspection and agricultural AI is surprisingly sparse and recent (2023–2025):

- **Plant Pathology OSR:** Meng et al. (2023, *Computers and Electronics in Agriculture*, DOI: `10.1016/j.compag.2023.108408`) evaluated known and unknown class recognition on plant leaves using distance-based thresholds. Verawati et al. (2025, *RESTI*, DOI: `10.29207/resti.v9i4.6525`) applied OpenMax to potato leaf diseases. Fuentes et al. (2023, *Acta Horticulturae*, DOI: `10.17660/ActaHortic.2023.1360.8`) investigated Open-Set Domain Adaptation (OSDA) in greenhouse monitoring.
- **Fruit Quality & Sorting OSR:** The overwhelming majority of fruit sorting systems (e.g., Apple, Banana, Orange grading) remain stubbornly closed-set. A few recent anomaly detection studies (e.g., *Plant Phenomics*, 2024) utilize hyperspectral imaging (HSI) with one-class autoencoders. However, standard RGB camera systems in commercial packing sheds almost universally enforce closed-set softmax classification.

### 2.2 Deep Dive into Formalin & Chemical Adulteration Detection Systems

| Study | Authors & Venue | Year | Methodology | Dataset & Setup | Closed vs Open Set? | Critical Scientific Limitations |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **FruitVision** | Bijoy et al., *Data in Brief* (`10.1016/j.dib.2025.111752`) | 2025 | Standard CNN baselines (VGG, ResNet, DenseNet, MobileNet) | 10,154 images (Apple, Banana, Orange, Grape, Mango); Fresh, Rotten, Formalin-mixed | **Strictly Closed-Set** (3 classes per fruit, trained supervised) | Does not test unseen adulterants; assumes formalin samples are labeled during training. |
| **DurbeenNet** | Sattar et al., *Heliyon* (`10.1016/j.heliyon.2024.e25371`) | 2024 | Custom CNN with multi-scale receptive fields (DurbeenNet) | Multi-fruit dataset; Fresh vs Formalin-treated | **Strictly Closed-Set** (Binary classification per fruit) | Evaluated only with random i.i.d. splits; high risk of background leakage; 96.7% accuracy reflects surface texture overfitting. |
| **SA-CoViT-XAI** | Saranya et al., *Food Analytical Methods* (`10.1007/s12161-025-02892-x`) | 2025 | CoAtNet (CNN-Transformer hybrid) + Simulated Annealing + Grad-CAM | Multi-class fruit quality (Fresh, Rotten, Formalin-mixed) | **Strictly Closed-Set** (Supervised 3-class classification) | Over-parameterized model (99.6% accuracy); Grad-CAM shows focus on fruit stems and illumination glares rather than verified chemical sites. |
| **ToxiFruit** | Sattar et al., *Scientific Data* (`10.1038/s41597-026-08185-0`) | 2026 | Dataset release with baseline deep learning benchmarks | 7,200 raw images (28,800 augmented) across 4 fruits (Apple, Malta, Mango, Banana) | **Strictly Closed-Set** (8 classes: Fresh vs Chemically Mixed) | Focuses entirely on closed-set discrimination; no OOD rejection, no selective prediction. |
| **IoT Gas Sensor Systems** | Various (e.g., *SEEJPH* `10.70135/seejph.vi.6183`, *UJAR* `10.13189/ujar.2022.100509`) | 2022–2025 | MQ-138 / HCHO semiconductor gas sensors + Arduino/RPi | Gas vapor concentration parts-per-million (ppm) | **Chemical Assay (Closed-Set Regression)** | Measures actual formaldehyde gas vapor in sealed chambers, but completely distinct from RGB vision. |

### 2.3 Key Verification Finding
**Open-set rejection of unseen formalin-mixed fruit conditions has NEVER been demonstrated.**
Every existing paper in this space treats formalin adulteration as a *known supervised class*. If a classifier is trained *only* on standard organic fresh and rotten fruits (the typical operational reality of an agricultural warehouse) and is then confronted with an adulterated fruit lot, **existing literature provides zero evidence on whether such fruits can be detected as Out-of-Distribution anomalies.**

---

## 3. Biophysical Reality: What Can RGB Cameras Actually Detect?

### 3.1 The Chemical Impossibility of Direct Formalin Vision
- **Chemical Structure:** Formaldehyde ($H-CHO$) has a molecular weight of 30.03 g/mol. In commercial trade, "formalin" is an aqueous solution (37% formaldehyde, 10–15% methanol stabilizer).
- **Optical Absorption:** Pure formaldehyde solution is completely transparent in the visible light spectrum ($\lambda \approx 400 - 700\text{ nm}$). Its primary vibrational absorption bands occur in the Mid-Infrared (MIR, $\sim 3.5\ \mu\text{m}$ and $5.8\ \mu\text{m}$) and Ultraviolet (UV, $\sim 280 - 320\text{ nm}$).
- **Conclusion:** Standard RGB camera sensors (Bayer filters capturing Red $\sim 650\text{ nm}$, Green $\sim 530\text{ nm}$, Blue $\sim 460\text{ nm}$) have **zero physical sensitivity** to the chemical bonds of formaldehyde.

### 3.2 What Manifests on the Fruit Surface?
When fruits are submerged in or sprayed with 10% formalin (as described in the *FruitVision* and *ToxiFruit* protocols):
1. **Protein Cross-Linking:** Formaldehyde cross-links epidermal proteins, hardening the outer peel and arresting natural cellular respiration.
2. **Inhibition of Enzymatic Browning:** Polyphenol oxidase (PPO) activity is halted, resulting in an unnaturally preserved, pale, or waxy appearance while the inner mesocarp gradually degenerates.
3. **Surface Glaze & Drying Artifacts:** Rapid evaporation leaves residual micro-crystals and altered specular reflections (unnatural gloss under directional lighting).
4. **Epidermal Shriveling:** Over 4–7 days, the skin develops non-standard microscopic striations different from natural fungal sporulation (which characterizes natural rot).

### 3.3 The Pseudoscience Risk & Methodological Boundary
If our paper claims: *"Our vision model detects formalin on fruit surfaces,"* reviewers with chemical or food-science expertise will reject the paper with prejudice.
However, if our paper claims:
> *"In safety-critical post-harvest intake, automated classifiers must distinguish between known standard conditions (Fresh vs Rotten) and unknown anomalies. Chemically adulterated fruits exhibit anomalous morphological and reflective deviations. We formulate this task as Open-Set Condition Rejection, testing whether OOD detection mechanisms can flag such contaminated lots for mandatory lab confirmation without ever having seen chemical adulterants during training."*

This formulation is methodologically bulletproof, scientifically honest, and addresses a massive real-world gap.

---

## 4. Architectural Analysis: The Proposed "Dual-Gate" Framework

The proposal suggests a multi-component pipeline:
$$\text{Input } x \longrightarrow \Big[\text{Gate 1: OOD Rejection}\Big] \longrightarrow \Big[\text{Gate 2: Calibrated Selective Prediction}\Big] \longrightarrow \text{Decision}$$

### 4.1 Decomposition of the Technical Components
1. **Closed-Set Feature Extractor:** A backbone $f_\theta(x) \in \mathbb{R}^d$ (e.g., MobileNetV2) trained on $K=6$ known fresh/rotten classes.
2. **Energy-Based OOD Scoring (Gate 1):**
   $$E(x; T) = -T \cdot \log \sum_{k=1}^K \exp\left(\frac{z_k(x)}{T}\right)$$
   Unlike Maximum Softmax Probability (MSP), free energy aligns with the log-marginal density $-T \log p(x)$ and does not suffer from softmax normalization inflation on distant out-of-distribution inputs.
3. **Feature-Space Mahalanobis Distance (Gate 1 Alternative / Complement):**
   $$D_M(x) = \min_k (f(x) - \mu_k)^T \Sigma^{-1} (f(x) - \mu_k)$$
   Measures structural deviation from the class-conditional Gaussian centroids in penultimate embedding space.
4. **Temperature-Scaled Class-Conditional Calibration (Gate 2):**
   $$P(y=k \mid x, \text{accepted}) = \frac{\exp(z_k / T_k)}{\sum_{j=1}^K \exp(z_j / T_j)}$$
5. **Selective Prediction Thresholding (Gate 2):**
   Abstain if $\max_k P(y=k \mid x) < \tau_{\text{cov}}$, routing the fruit to human manual inspection or chemical benchtop testing.

### 4.2 Is Combining These Two Methods a Novel Algorithm?
**Brutally Honest Answer:** **NO.**
Cascaded OOD detection and selective classification (abstention) have been proposed in general machine learning (e.g., Geifman & El-Yaniv 2017, 2019; Liu et al. 2020; Yang et al. 2021). Combining an energy score with temperature scaling is a standard engineering assembly. If submitted to a tier-1 pure ML venue (NeurIPS, ICML), claiming the dual-gate architecture as a novel algorithmic contribution would be dismissed as incremental.

### 4.3 Where Does Genuine Novelty Lie?
For an applied machine learning and data engineering venue (*ICMLDE 5.0 / Procedia Computer Science*), the contribution is **not** an invention of a new activation function or loss formulation. The contribution lies in:
1. **The First Systematic Benchmark of Open-Set Rejection for Unknown Post-Harvest Food Safety Hazards:** Proving empirically whether standard closed-set models can or cannot withstand adulterated condition shifts.
2. **The Asymmetric Risk-Coverage Formulation for Food Safety:** Formalizing an asymmetric cost matrix where accepting an unknown/adulterated fruit as "Fresh" carries a catastrophic penalty ($C_{\text{hazard}} \gg C_{\text{reject}}$).
3. **Cross-Dataset and Cross-Condition Disentanglement:** Disentangling *Covariate Shift on Knowns* (e.g., Fresh apples from a different country) from *Semantic Shift on Fruit Types* (e.g., Mangos/Grapes) and *Condition Shift on Adulteration* (e.g., Formalin dipping).

---

## 5. Feasibility Verdict

The proposed research question is **exceptionally strong, timely, and publishable**, provided we adhere strictly to the following parameters:
- **Do NOT** claim optical chemical sensing.
- **Do NOT** claim to have invented the individual mathematical equations of Energy OOD or Temperature Scaling.
- **DO** frame the work as a rigorous, leakage-safe empirical study of **Risk-Aware Open-Set Screening under Multi-Dataset Domain Shift**.

