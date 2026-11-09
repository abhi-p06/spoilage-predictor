# State of the Art: Multi-Modal Post-Harvest Quality & Logistics AI

> **Document:** `literature_review/04_State_of_the_Art.md`  
> **Auditor/Analyst:** AgriRoute Literature Specialist  
> **Scope:** Critical review of published state-of-the-art across four core technical domains (2020–2026).

---

## 1. Deep Learning Architectures for Visual Fruit Quality Assessment

Visual quality grading of harvested horticultural produce has evolved rapidly from classical hand-crafted color-histogram and texture-descriptor methods (e.g. GLCM, SIFT) toward deep convolutional and attention-based neural backbones (Rizzo et al., 2023).

### 1.1 Lightweight Inverted Residual Architectures (MobileNetV2)
MobileNetV2 (Sandler et al., 2018) is established as the premier lightweight backbone for edge agricultural inspection. Its architectural innovation—the inverted residual block with linear bottlenecks—expands feature representations to high dimensions via $1 \times 1$ point-wise convolutions, filters them through $3 \times 3$ depthwise separable convolutions, and projects back to a low-dimensional manifold without non-linearities:
- **Parameter Efficiency:** MobileNetV2 requires only 2.26M to 3.4M parameters and approximately 300M to 314M multiply-accumulate operations (MACs).
- **Agricultural Performance:** Chen et al. (2024) achieved 95.42% accuracy on agricultural defect detection using a modified MobileNetV2 with coordinate attention. Gulzar (2023) achieved 96.7% classification accuracy on curated fruit ripeness classes.
- **Edge Deployment:** Benchmark latency on non-GPU mobile CPUs ranges from 18ms to 24ms per frame, making it fully viable for real-time mobile and edge deployments.
- **Vulnerabilities:** Due to aggressive channel compression in linear bottlenecks, MobileNetV2 struggles to preserve fine spatial details, frequently missing early-stage pinpoint surface rot (e.g. initial *Penicillium expansum* sporulation on apple skin).

### 1.2 Compound-Scaled Architectures (EfficientNet-B0)
Tan & Le (2019) demonstrated that traditional heuristic scaling of neural networks (arbitrarily scaling only depth as in ResNet, or only resolution) yields sub-optimal accuracy-to-compute ratios. EfficientNet introduces principled **compound scaling**, scaling depth ($\alpha^\phi$), width ($\beta^\phi$), and resolution ($\gamma^\phi$) simultaneously under a fixed resource budget:
- **Compute Efficiency:** EfficientNet-B0 achieves 77.1% top-1 accuracy on ImageNet with 5.3M parameters and 0.39 GFLOPs, matching the accuracy of ResNet50 (23.58M parameters, 3.86 GFLOPs) at a fraction of the compute.
- **Agricultural Benchmark:** Hassan et al. (2025) fine-tuned EfficientNet-B0 for apple pathology detection, achieving 98.41% accuracy. The MBConv blocks (Mobile Inverted Bottlenecks with Squeeze-and-Excitation attention) capture both global morphological contours and localized skin necrosis with high fidelity.

### 1.3 Deep Residual Baselines (ResNet50)
He et al. (2016) introduced identity shortcut connections ($F(x) + x$) to solve the degradation and vanishing gradient problem in deep networks. ResNet50 remains the gold-standard benchmark in computer vision literature:
- **Representational Depth:** 50 convolutional layers grouped into 4 residual stages with bottleneck blocks ($1 \times 1, 3 \times 3, 1 \times 1$).
- **Limitations in Agri-Logistics:** ResNet50 requires 23.58M parameters and 3.86 GFLOPs. On embedded CPU targets (e.g. Raspberry Pi 4 or smartphone edge processors), inference latency exceeds 60ms to 90ms, causing thermal throttling and rapid battery drain during high-throughput field inspection.

---

## 2. Uncertainty Quantification & Probability Calibration in Food Inspection

In safety-critical agricultural inspection and logistics dispatch, classification accuracy alone is an insufficient metric. A model that predicts a high confidence score on an out-of-distribution or ambiguous sample can cause severe downstream supply-chain disruptions.

### 2.1 The Overconfidence Problem & ECE
Guo et al. (2017) demonstrated that while modern architectural innovations (depth, width, batch normalization, weight decay) have steadily driven top-1 error rates down, they have simultaneously degraded **probability calibration**. Softmax outputs no longer reflect the empirical probability of correct classification.

Calibration error is formally quantified by **Expected Calibration Error (ECE)**. The prediction space $[0, 1]$ is partitioned into $M$ equally spaced bins $B_m$. The ECE is the weighted average difference between empirical bin accuracy $\text{acc}(B_m)$ and average bin confidence $\text{conf}(B_m)$:
$$\text{ECE} = \sum_{m=1}^M \frac{|B_m|}{N} \bigl|\text{acc}(B_m) - \text{conf}(B_m)\bigr|$$

The **Brier Score** measures mean squared calibration error:
$$\text{BS} = \frac{1}{N} \sum_{i=1}^N \sum_{k=1}^K (f_{ik} - y_{ik})^2$$

### 2.2 Post-Hoc Temperature Scaling
Temperature scaling (Guo et al., 2017) is a post-processing technique that rescales logit vector $\mathbf{z}_i$ by a learned scalar temperature $T > 0$:
$$\hat{p}_i = \max_{k} \sigma\left(\frac{\mathbf{z}_i}{T}\right)_k$$
- The parameter $T$ is optimized on a held-out validation set via Negative Log-Likelihood (NLL).
- Because $T$ is applied monotonically across all logits, the argmax prediction is strictly preserved ($\Delta \text{Accuracy} = 0$), while probabilities become well-calibrated.
- Kim et al. (2026) showed that post-hoc calibration reduced ECE in agricultural neural networks by 62%, proving that temperature scaling is computationally negligible yet crucial for automated agricultural decision-making.

---

## 3. Post-Harvest Deterioration Kinetics & Cold-Chain Exposure

Produce deterioration is not a linear function of time, but a non-linear biochemical process driven by cumulative environmental exposure (Kader, 2002; USDA Handbook 66).

### 3.1 Biochemical Ripening & Respiration Kinetics
Climacteric fruits (apples, bananas, mangoes, tomatoes) exhibit a sharp peak in respiration rate ($\text{mg } CO_2 / \text{kg}\cdot\text{hr}$) and ethylene synthesis ($C_2H_4$) at the onset of ripening. Non-climacteric produce (citrus, grapes) deteriorates via steady senescence without a climacteric respiratory surge.

The rate of enzymatic tissue degradation follows the **Arrhenius law**:
$$k(T) = A \exp\left(-\frac{E_a}{R T}\right)$$
- Every $10^\circ\text{C}$ increase in ambient transport temperature ($Q_{10}$ temperature coefficient) typically doubles or triples the rate of respiration and spoilage ($Q_{10} \approx 2.0\text{--}3.5$).
- A 4-hour refrigeration breakdown during transit at $32^\circ\text{C}$ can consume more effective shelf life than 48 hours of compliant transit at $4^\circ\text{C}$.

### 3.2 In-Transit IoT Telemetry Integration
Ali et al. (2023) demonstrated that integrating continuous temperature, relative humidity, and $CO_2$ streams from transit loggers into Arrhenius models predicted remaining shelf life with an MAE of 0.82 days. However, existing sensor models suffer from a fundamental limitation: **they assume uniform initial produce quality at the loading dock**. If a batch of fruit is already 30% spoiled upon loading, a sensor monitoring perfect cold-chain transit temperatures will catastrophically overestimate remaining shelf life.

---

## 4. Dynamic Vehicle Routing Problems Under Perishability (DVRP-P)

### 4.1 Classical Static Routing vs. Dynamic Perishable Routing
Classical logistics models optimize the Vehicle Routing Problem (VRP) or Vehicle Routing Problem with Time Windows (VRPTW) by minimizing total travel distance or fuel cost. In agricultural cold chains, this formulation is fundamentally flawed because cargo is an active, decaying biological asset.

Esteso et al. (2021) and Pérez Lechuga et al. (2024) formalized the **Vehicle Routing Problem under Perishability (VRP-P)**:
- Cargo economic value decays non-linearly over transit duration $t$:
  $$V_{\mathrm{cargo}}(t) = V_0 \cdot \bigl(1 - \text{Risk}(t)\bigr)$$
- Delivery rejection occurs if freshness falls below a commercial threshold $F_{\min}$ upon arrival at customer node $j$.
- Li et al. (2026) developed dynamic risk-aware ant colony optimization, showing that dynamically re-routing vehicles to nearer secondary processing markets upon thermal abuse events reduced total lost cargo by 28.4% compared to static shortest-path routing.

### 4.2 The Multi-Modal Coupling Gap
Existing DVRP-P systems (Li et al., 2026; Esteso et al., 2021) rely exclusively on mathematical simulations with assumed initial quality values ($V_0 = 1.0$). **None of these routing systems are coupled with computer vision at the point of loading.** 

Conversely, computer vision studies (Gulzar, 2023; Chen et al., 2024) classify fruit quality in isolation, completely detached from transit logistics, road networks, or market price dynamics.

Closing this gap—by feeding a calibrated, edge-feasible visual quality score directly into a perishability-aware dynamic routing and market selection framework—represents the definitive frontier of post-harvest loss research.

