# Section II: Related Work and Academic Foundations

*(Drafted for the AgriRoute Academic Revision — Procedia Computer Science / Elsevier Format)*

---

Post-harvest food loss in horticultural supply chains remains a critical driver of economic instability and food insecurity, particularly in emerging economies where smallholder farmers lack real-time decision-support tools [1]. While recent advances in deep learning, Internet of Things (IoT) cold-chain telemetry, and vehicle routing have addressed individual facets of the supply chain, existing literature exhibits persistent silos between pre-dispatch quality assaying, in-transit degradation modeling, and dynamic economic dispatch. This section reviews relevant literature across these foundational domains, highlights critical methodological limitations, and establishes the precise research questions guiding AgriRoute.

---

## 1. Deep Learning for Visual Produce Grading and Freshness Assessment

Automated visual inspection of harvested fruits and vegetables has transitioned from classical hand-crafted color histograms and texture descriptors (e.g., Gray-Level Co-occurrence Matrices) toward deep convolutional neural networks (CNNs) [2]. A recent comprehensive survey by Rizzo et al. [2] established that over 85% of modern fruit ripeness and quality studies utilize transfer learning from ImageNet-pretrained backbones, consistently outperforming models trained from scratch by 6% to 12% in top-1 classification accuracy.

Among edge-deployable architectures, MobileNetV2 [16] has become a dominant baseline due to its inverted residual blocks and depthwise separable convolutions, which constrain computational complexity to approximately 300M multiply-accumulate operations (MACs). Gulzar [4] achieved 96.7% accuracy on curated fruit ripeness categories using fine-tuned MobileNetV2, while Chen et al. [3] reported 95.42% accuracy on agricultural product defects using coordinate-attention MobileNetV2 with a 22ms inference latency on commodity CPUs. Concurrently, compound-scaled architectures such as EfficientNet-B0 [17] have emerged as competitive alternatives. Hassan et al. [9] demonstrated that EfficientNet-B0 matches or exceeds the representational capacity of ResNet50 [18] (achieving 98.41% accuracy on apple disease benchmarks) while requiring 5.7x fewer parameters (4.05M vs. 23.58M) and 9.4x fewer FLOPs (0.39 GFLOPs vs. 3.86 GFLOPs). Furthermore, Zhang et al. [5] showed that multi-task CNNs can simultaneously predict categorical produce identity and a continuous freshness index ($R^2 > 0.94$).

However, the computer vision literature in post-harvest quality assessment suffers from two systemic flaws:
1. **Isolated Static Inspection:** Models are universally evaluated as isolated, stationary sorting kiosks at packing facilities [2, 5], completely disconnected from subsequent transport transit dynamics or destination market economics.
2. **Surface Visual Latency:** As established in post-harvest physiology [12, 13], surface RGB imaging captures visual symptoms (browning, fungal mycelia, skin wrinkling) that inherently lag internal biochemical degradation (pectin solubilization, ethylene-triggered enzymatic softening) by 24 to 72 hours in thick-skinned produce.

---

## 2. Domain Generalization and Cross-Dataset Robustness

A second major deficiency in current agricultural vision literature is the failure to evaluate out-of-distribution (OOD) generalization across distinct capture environments, camera sensors, and natural lighting regimes [10, 11].

Recent critical audits by Jafar et al. [10] and Hilal et al. [11] reveal that deep agricultural vision models trained on curated, studio-captured datasets (such as Fruits-360 [14] or Kaggle Fruit Fresh/Rotten) suffer severe performance collapse—often dropping 25% to 45% in Macro F1 score—when deployed on in-situ farm or market images (e.g., the FIDS30 benchmark). Gulzar et al. [15] corroborated this vulnerability empirically, observing a 31.4% drop in classification F1 when a MobileNetV2 trained on curated images was evaluated on field-collected produce photos.

Furthermore, Hilal et al. [11] discovered that over 32% of popular open agricultural image datasets contain identical or near-duplicate images across pre-divided training and test partitions due to video turntable burst captures. Models evaluated on these contaminated splits exhibit artificially inflated accuracies that fail to replicate in real-world deployment. To establish authentic scientific validity, models must be evaluated on leak-free partitions audited via perceptual hashing (pHash) and tested zero-shot across external datasets [1, 11].

---

## 3. Probability Calibration and Uncertainty in Agricultural Decision-Making

In high-stakes logistics dispatch—where an algorithmic alert can trigger vehicle diversion or cargo disposal—classification accuracy alone is an insufficient criterion. Decision engines require **calibrated probabilities** that reflect true empirical risk [15].

Guo et al. [15] proved that modern deep neural networks with batch normalization and high representational depth are chronically overconfident: a model outputting a softmax probability of $\hat{p} = 0.95$ often achieves less than 75% empirical accuracy on held-out or shifted distributions. Calibration error is conventionally quantified using Expected Calibration Error (ECE) and Brier Score [15]. While post-hoc calibration techniques such as Temperature Scaling have achieved widespread adoption in medical imaging and autonomous driving, their application to post-harvest agriculture remains remarkably rare [12]. Kim et al. [12] recently demonstrated that temperature scaling reduced ECE by 62% in agricultural neural networks, confirming that uncalibrated raw softmax scores distort downstream decision boundaries unless explicitly calibrated against validation log-likelihoods.

---

## 4. Post-Harvest Deterioration Kinetics and In-Transit Cold-Chain Tracking

Produce deterioration during transit is governed by non-linear biochemical kinetics driven by cumulative environmental exposure [12, 13]. Climacteric produce (such as apples, bananas, and tomatoes) undergoes a pronounced respiratory climacteric, where respiration rate and ethylene synthesis accelerate under ambient temperature according to the Arrhenius law [7, 13]:
$$k(T) = A \exp\left(-\frac{E_a}{R T}\right)$$

Every $10^\circ\text{C}$ rise in transport temperature ($Q_{10}$ coefficient $\approx 2.0\text{--}3.0$) doubles or triples the rate of biochemical decay [13]. Ali et al. [7] integrated in-transit wireless IoT telemetry (temperature, relative humidity, $CO_2$) into Arrhenius shelf-life equations, predicting remaining transit shelf life with a Mean Absolute Error (MAE) of 0.82 days across 45 commercial shipments.

However, existing IoT tracking systems operate under a fatal assumption: **they assume uniform, pristine produce quality at the time of loading ($V_0 = 1.0$)** [7]. If produce has already sustained latent visual or pathological decay prior to transit, standard cold-chain monitoring severely overestimates remaining shelf life, failing to anticipate premature rot.

---

## 5. Dynamic Vehicle Routing Under Perishability and Commercial Platforms

In operations research, the Vehicle Routing Problem under Perishability (VRP-P) incorporates shelf-life decay into logistics dispatch [6, 8, 20]. Esteso et al. [8] developed mixed-integer linear programming formulations for perishable citrus supply chains, showing that perishability-aware dispatch prevented 18.6% of product waste compared to distance-only shortest-path dispatch. More recently, Li et al. [6] applied dynamic risk-aware ant colony optimization to cold-chain distribution, demonstrating that dynamic in-transit rerouting to secondary salvage markets upon refrigeration failure reduced total cargo spoilage loss by 28.4%.

Commercial agri-logistics platforms have attempted to address supply-chain inefficiencies, but remain fragmented:
- **Upstream Quality Platforms (e.g., AgNext Qualix, Intello Labs):** Provide automated visual assaying at mandis or export terminals, but rely on expensive proprietary hardware kiosks ($> \$5,000$) and cease tracking once cargo departs the loading dock.
- **In-Transit Telemetry Platforms (e.g., Ecozen Eco-Frost, Stellapps):** Provide cold-room or fleet GPS tracking, but operate without visual defect assessment.

---

## 6. Synthesis: The Unaddressed Research Gap

As synthesized in Table I, existing literature exhibits a fundamental structural disconnect:
- Computer vision research grades fruit quality in stationary isolation without logistics coupling [2, 4, 5].
- Cold-chain IoT models track ambient transport temperature while assuming uniform initial produce quality [7].
- Operations research algorithms optimize vehicle routes using theoretical decay equations without empirical visual or sensor inputs [6, 8].

**AgriRoute addresses this definitive gap.** By coupling an uncertainty-calibrated, edge-feasible visual classifier at dispatch with cumulative transit exposure and real-time government mandi market price feeds (AGMARKNET), AgriRoute establishes the first unified, closed-loop decision framework for perishable produce salvage.

---

## 7. The Three Defensible Research Questions for AgriRoute

Guided by this literature gap and the reviewer feedback from ICMLDE 5.0, the revised AgriRoute study is anchored upon three verifiable, empirical research questions:

> ### **Research Question 1 (Edge Vision & Out-of-Distribution Robustness):**
> *How do edge-optimized convolutional architectures (MobileNetV2, EfficientNet-B0) compare against standard residual baselines (ResNet50) in classification accuracy, parameter footprint, and inference latency when classifying post-harvest produce freshness on leak-free partitions, and to what extent does performance degrade when evaluated zero-shot on out-of-distribution external datasets?*
>
> *(Hypothesis: EfficientNet-B0 achieves competitive Macro F1 with ResNet50 while matching MobileNetV2's edge viability; zero-shot external evaluation exhibits an empirical domain drop of $15\text{--}30\%$ driven by illumination and background shifts.)*

> ### **Research Question 2 (Uncertainty Calibration & Decision Thresholding):**
> *Does post-hoc temperature scaling reliably minimize the Expected Calibration Error (ECE) and Brier Score of edge produce freshness classifiers across varying domain shifts, and does probability calibration eliminate overconfident false-alarm dispatch recommendations in downstream risk alerting?*
>
> *(Hypothesis: Raw softmax scores exhibit severe overconfidence with $\text{ECE} > 0.08$; post-hoc temperature scaling reduces $\text{ECE} < 0.03$ without altering classification accuracy, stabilizing operational traffic-light alert boundaries.)*

> ### **Research Question 3 (Multi-Modal Risk Coupling & Economic Salvage Value):**
> *Does a closed-loop multi-modal decision engine coupling pre-dispatch visual freshness scores with in-transit transport exposure achieve statistically significant reductions in post-harvest economic loss compared to decoupled visual-only and distance-only routing baselines under simulated cold-chain disturbances?*
>
> *(Hypothesis: Joint multi-modal risk optimization significantly preserves delivered cargo value over decoupled baselines ($p < 0.01$ via Wilcoxon signed-rank test), exhibiting a convex cost minimum across the fusion sensitivity parameter $\alpha \in [0.0, 1.0]$.)*

