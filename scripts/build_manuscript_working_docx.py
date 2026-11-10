#!/usr/bin/env python3
"""
scripts/build_manuscript_working_docx.py
========================================
Assembles the working Word manuscript 'research_paper/manuscript/manuscript_working.docx'
using the clean Elsevier Procedia Computer Science template
('research_paper/template/PROCS_ICMLDE_2026_Templates_clean.docx').

Ensures exact compliance with:
- 192 mm x 262 mm single-column page layout
- Elsevier paragraph styles: 'Els-Title', 'Els-Author', 'Els-Affiliation',
  'Els-Abstract-head', 'Els-Abstract-text', 'Els-keywords', 'Els-1storder-head',
  'Els-2ndorder-head', 'Els-body-text', 'Els-bulletlist', 'Els-numlist',
  'Els-reference-head', 'Els-reference'.
- 20 verified references in Vancouver style ([1] - [20]).
"""

import os
from pathlib import Path
import docx

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = PROJECT_ROOT / "research_paper" / "template" / "PROCS_ICMLDE_2026_Templates_clean.docx"
OUTPUT_PATH = PROJECT_ROOT / "research_paper" / "manuscript" / "manuscript_working.docx"


def build_manuscript():
    doc = docx.Document(str(TEMPLATE_PATH))

    # P00: DocHead (Preserve Conference Header)
    # P01: Title
    doc.paragraphs[1].text = "Source-Stratified Evaluation of Open-Set Fruit Image Classification Under Species and Treatment-Associated Shifts"
    # P02: Author
    doc.paragraphs[2].text = "Project Research Team"
    # P03: Affiliation
    doc.paragraphs[3].text = "AgriRoute Research Consortium, Department of Computer Engineering"
    # P04: Track / Submission Identifier
    doc.paragraphs[4].text = "5th International Conference on Machine Learning and Data Engineering (ICMLDE 2026) — Paper ID: 1345"
    # P05: Abstract Head
    doc.paragraphs[5].text = "Abstract"

    # P06: Abstract Body
    abstract_text = (
        "Automated fruit-quality classification using computer vision can achieve strong performance on familiar image "
        "distributions but may become unreliable under changes in data sources, fruit species, and post-harvest treatment "
        "conditions. This study presents a source-stratified empirical evaluation of a frozen MobileNetV2-based six-class "
        "fruit-quality classifier and multiple out-of-distribution (OOD) detection approaches. The evaluation uses 13,465 "
        "image records from three image repositories, organized into primary in-distribution, external known-class, "
        "unseen-species, treatment-labelled, and combined-shift cohorts.\n\n"
        "Five established OOD scoring approaches—Maximum Softmax Probability (MSP), Energy, ODIN, Mahalanobis distance, "
        "and OpenMax—are compared with an operational Energy–MSP dual-gate cascade. Closed-set accuracy decreases from "
        "96.92% on the primary test partition to 68.36% on the pooled external known-class partition, demonstrating "
        "substantial performance degradation under external data shifts. Within the FruitVision repository, Energy achieves "
        "an AUROC of 81.57% for the known-versus-unseen-species comparison, while the corresponding operational false acceptance "
        "rate is 13.18%. Performance varies across repositories, with Energy achieving 67.52% AUROC on the source-matched "
        "Sultana unseen-species comparison. More importantly, discrimination between natural known-class images and "
        "treatment-labelled known-class images is weak, with Energy achieving 53.13% AUROC. Under the fixed dual-gate operating "
        "thresholds, 42.83% of the treatment-labelled images are accepted and assigned a Fresh class.\n\n"
        "The findings demonstrate that OOD detection performance depends strongly on the evaluated shift and data source. "
        "They also show that RGB image classification alone cannot reliably distinguish the evaluated treatment-labelled "
        "condition. The study provides an image-level benchmark analysis with source-stratified comparisons, uncertainty "
        "estimates, duplicate-sensitivity analysis, and explicit limitations concerning dataset labels, specimen independence, "
        "and real-world validation."
    )
    doc.paragraphs[6].text = abstract_text

    # P07: Keywords
    doc.paragraphs[7].text = (
        "Keywords: Fruit quality classification; Open-set recognition; Out-of-distribution detection; "
        "Domain shift; MobileNetV2; Energy-based detection; Image classification; Food quality assessment."
    )

    # P08: Section 1 Header
    doc.paragraphs[8].text = "1. Introduction"

    # Remove paragraphs 9 to end and clear template tables
    p_elements_to_remove = [p._element for p in doc.paragraphs[9:]]
    for elem in p_elements_to_remove:
        elem.getparent().remove(elem)

    for table in list(doc.tables):
        table._element.getparent().remove(table._element)

    # Helper function to add paragraph with style
    def add_p(text, style="Els-body-text"):
        return doc.add_paragraph(text, style=style)

    # --- 1.1 Research Background and Motivation ---
    add_p("1.1. Research Background and Motivation", style="Els-2ndorder-head")
    add_p(
        "Post-harvest agricultural loss represents a critical challenge for global food security, economic stability, "
        "and supply chain sustainability [1]. According to the Food and Agriculture Organization (FAO), approximately "
        "one-third of all horticultural produce harvested worldwide is lost or degraded between the farm gate and retail "
        "distribution [1]. In agrarian economies, post-harvest deterioration across domestic transit corridors is particularly "
        "acute. Nationwide surveys in India conducted by the Indian Council of Agricultural Research (ICAR-CIPHET) indicate "
        "that cumulative post-harvest losses in commercial fruits—such as apples, bananas, and citrus—consistently range "
        "between 6.7% and 15.9% [2]. These losses disproportionately penalize smallholder producers and aggregation packhouses, "
        "where produce sorting and quality grading have historically relied upon manual, visual inspection. Manual grading is "
        "inherently subjective, labour-intensive, prone to operator fatigue, and incapable of scaling to high-throughput sorting "
        "facilities [3], [4]."
    )
    add_p(
        "In response to these operational bottlenecks, computer vision and deep learning have emerged as promising non-destructive "
        "methodologies for automated fruit freshness assessment, ripeness grading, and surface defect classification [3]–[6]. "
        "Convolutional neural networks (CNNs), particularly lightweight architectures such as MobileNetV2 [7], have become central "
        "to practical agricultural deployments. Depthwise separable convolutions and inverted residual bottlenecks allow MobileNetV2 "
        "to execute on resource-constrained mobile phones and edge sorting devices with parameter budgets under 4 million weights [5], [7]. "
        "In controlled academic benchmarks, modern visual classifiers routinely report top-1 accuracy exceeding 95% across multi-class "
        "produce datasets [4]–[6]."
    )

    # --- 1.2 The Closed-Set Assumption and Its Vulnerabilities ---
    add_p("1.2. The Closed-Set Assumption and Its Vulnerabilities in Agricultural Vision", style="Els-2ndorder-head")
    add_p(
        "Despite high benchmark accuracy, practical deployment of deep learning models in real-world agricultural environments encounters "
        "fundamental reliability barriers. Standard supervised image classifiers operate under a strict closed-set assumption: the training, "
        "validation, and operational deployment data are presumed to be independent and identically distributed (i.i.d.) over a fixed, "
        "finite set of semantic classes, Y = {1, 2, ..., K} [8], [9]. In operational agricultural workflows, however, this assumption "
        "is persistently violated. Vision models deployed at packhouses, retail terminals, or farm collection centres confront three distinct, "
        "compounding categories of distribution shift:"
    )
    add_p(
        "• Covariate and Domain Shift: Images collected in real-world environments exhibit pronounced variations in background illumination, "
        "sensor optics, specular glare, ambient shadows, and post-harvest handling marks that differ markedly from laboratory studio "
        "benchmarks [3], [5]. Furthermore, biological cultivar diversity—such as regional Asian apple varieties differing in pigmentation "
        "and epidermal russeting from Western commercial cultivars—induces domain shifts that severely degrade feature representations [17].",
        style="Els-bulletlist"
    )
    add_p(
        "• Semantic Shift (Unseen Species): In automated sorting lines, bins, or field crates, models trained exclusively on a small palette "
        "of target crops (e.g., apple, banana, and orange) frequently encounter non-target produce species (e.g., mango, guava, jujube, "
        "pomegranate, or grapes). Under standard closed-set inference, deep networks lack an explicit rejection mechanism; they are forced "
        "to assign an unseen species to one of the K known classes, often with uncalibrated, erroneously high confidence [8], [9].",
        style="Els-bulletlist"
    )
    add_p(
        "• Post-Harvest Treatment Condition Shift: Horticultural commodities in commercial trade are frequently subjected to post-harvest "
        "preservative treatments—such as fungicide dips, edible wax emulsions, or chemical fixatives like formalin—intended to retard "
        "visual senescence during extended transit or storage. When produce has undergone chemical treatment, superficial visual decay "
        "symptoms may be artificially masked or altered, breaking the standard relationship between visual appearance and true biological quality.",
        style="Els-bulletlist"
    )
    add_p(
        "Under standard softmax classification, neural networks are notoriously overconfident [8]. Logit outputs normalized via the softmax "
        "function produce probability distributions that often peak sharply near 1.0 even when the input image is heavily corrupted, "
        "semantically anomalous, or completely out-of-distribution [8], [9]. In agricultural supply chains, an overconfident false-positive "
        "classification—such as misclassifying an unseen non-target species or chemically treated decaying produce as 'Fresh'—presents "
        "severe commercial, food safety, and regulatory liabilities."
    )

    # --- 1.3 Open-Set Recognition and OOD Detection Foundations ---
    add_p("1.3. Open-Set Recognition and Out-of-Distribution Detection Foundations", style="Els-2ndorder-head")
    add_p(
        "To address closed-set failure modes, computer vision research has developed two closely related paradigms: Open Set Recognition "
        "(OSR) [10], [11] and Out-of-Distribution (OOD) Detection [9], [12]. The concept of open-set recognition was formalized by Scheirer "
        "et al. [10], who defined the objective as simultaneously classifying known training classes while bounding the open space risk—the "
        "risk of incorrectly labeling an unknown, novel class sample as any known class. Bendale and Boult [11] extended this concept to "
        "deep neural networks through OpenMax, which estimates the probability of an input belonging to an unknown class by fitting Weibull "
        "distributions to activation vectors in the penultimate layer."
    )
    add_p(
        "Simultaneously, the broader machine learning community formalized generalized out-of-distribution detection [9], [12]. Hendrycks "
        "and Gimpel [9] established the Maximum Softmax Probability (MSP) baseline, showing that correctly classified in-distribution samples "
        "typically exhibit higher maximum posterior probabilities than anomalous inputs. Liang et al. [13] developed ODIN, which amplifies "
        "the separation between in-distribution and out-of-distribution samples using temperature-scaled softmax outputs and input-space "
        "gradient perturbations. Lee et al. [14] introduced a feature-space Mahalanobis distance metric that models class-conditional Gaussian "
        "distributions across intermediate hidden representations. More recently, Liu et al. [15] proposed Energy-based OOD detection, utilizing "
        "the Helmholtz free energy function computed directly over unnormalized logits. Energy scores possess the theoretical advantage of "
        "being linearly aligned with the true input marginal probability density, avoiding the artificial probability saturation inherent in "
        "softmax normalization [12], [15]. Additionally, Vaze et al. [16] demonstrated that closed-set classifier capacity and representation "
        "quality strongly dictate open-set discrimination performance."
    )
    add_p(
        "In operational deployment, OOD detectors are typically implemented either as continuous ranking functions or as discrete rejection "
        "gates governed by a pre-calibrated threshold τ. When an input sample produces an anomaly score that violates the threshold, the system "
        "abstains from classification, triggering manual inspection or secondary non-optical assay."
    )

    # --- 1.4 Limitations of Existing Research and Specific Research Gaps ---
    add_p("1.4. Limitations of Existing Research and Specific Research Gaps", style="Els-2ndorder-head")
    add_p(
        "While OOD detection and agricultural computer vision are both mature disciplines, their intersection suffers from four critical "
        "scientific limitations:"
    )
    add_p(
        "• Gap 1: Over-Optimistic Internal-Split Benchmarks: The majority of existing fruit-freshness studies report classification and anomaly "
        "detection metrics computed exclusively on random train/test splits of a single, curated dataset (e.g., standard Kaggle archives) [4]–[6]. "
        "Recent audits reveal that random image partitioning in agricultural benchmarks frequently suffers from severe near-duplicate and affine "
        "leakage between training and testing sets, producing artificially inflated accuracies that fail to replicate under external domain shifts [17].",
        style="Els-bulletlist"
    )
    add_p(
        "• Gap 2: Confounded Cross-Dataset Evaluations: When external evaluations are conducted, researchers commonly evaluate unseen species drawn "
        "from a completely different repository than the known-class training cohort (e.g., training on Kaggle apples and testing on external repository "
        "grapes). This experimental design introduces severe cross-repository confounding: the detector's ability to reject the unseen species is "
        "driven largely by differences in camera hardware, studio lighting, and background compression rather than true biological or semantic "
        "divergence [12]. Without source-stratified benchmarks that evaluate known and unknown produce collected under identical repository "
        "conditions, the true semantic discrimination capacity of vision models remains unmeasured.",
        style="Els-bulletlist"
    )
    add_p(
        "• Gap 3: Complete Absence of Preservative Condition Shift Benchmarks: Existing open-set agricultural literature focuses almost exclusively "
        "on species discrimination (identifying novel fruits). It completely ignores post-harvest chemical preservation and treatment-labelled condition "
        "shifts. Whether standard RGB vision models and OOD scoring functions can distinguish naturally fresh produce from chemically treated fruits "
        "remains an unaddressed empirical question.",
        style="Els-bulletlist"
    )
    add_p(
        "• Gap 4: Retrospective Metric Optimism vs. Operational Threshold Reliability: Nearly all published OOD literature evaluates algorithms "
        "using threshold-free retrospective metrics, specifically the Area Under the Receiver Operating Characteristic curve (AUROC) and the False "
        "Positive Rate at 95% True Positive Rate (FPR@95) [9], [12], [15]. While informative for theoretical comparison, retrospective metrics "
        "assume oracle access to the entire test distribution. In real-world agricultural sorting, systems must operate prospectively with fixed "
        "thresholds pre-calibrated on internal validation sets. The degree to which fixed validation thresholds maintain acceptable Out-of-Distribution "
        "False Acceptance Rates (UFAR) without causing unacceptable In-Distribution Known-Class False Rejections (KRR) on external produce has not "
        "been rigorously quantified.",
        style="Els-bulletlist"
    )

    # --- 1.5 Research Objectives and Formal Research Questions ---
    add_p("1.5. Research Objectives and Formal Research Questions", style="Els-2ndorder-head")
    add_p(
        "This investigation addresses these foundational gaps by conducting an extensive, source-stratified empirical evaluation of "
        "out-of-distribution detection in fruit image classification. The study evaluates a frozen MobileNetV2 six-class visual classifier "
        "across N = 13,465 local benchmark image records curated from three distinct repositories under the Stage 4.0.3 external evaluation protocol. "
        "The paper specifically investigates three core research questions:"
    )
    add_p(
        "1. Research Question 1 (Cross-Repository Domain Shift): To what extent does cross-repository domain shift degrade the closed-set top-1 "
        "accuracy, macro-F1, and balanced accuracy of a lightweight MobileNetV2 vision backbone when transitioning from laboratory training "
        "distributions to external retail environments?",
        style="Els-numlist"
    )
    add_p(
        "2. Research Question 2 (Source-Stratified OOD Discrimination): How effectively do established OOD scoring mechanisms (MSP, Energy, "
        "ODIN, Mahalanobis distance, OpenMax) discriminate between in-distribution produce and distribution shifts when evaluated in source-matched "
        "cohorts isolating (a) unseen-species semantic shift, (b) treatment-labelled condition shift, and (c) combined species-and-treatment shifts?",
        style="Els-numlist"
    )
    add_p(
        "3. Research Question 3 (Operational Threshold Reliability): How reliably do fixed rejection thresholds—calibrated on internal validation "
        "data to maintain 95% known-class retention—control out-of-distribution false acceptance (UFAR) under real-world domain and condition "
        "shifts, and what operational penalty in known-class false rejection (KRR) is incurred on external produce?",
        style="Els-numlist"
    )

    # --- 1.6 Evidence-Supported Research Contributions ---
    add_p("1.6. Evidence-Supported Research Contributions", style="Els-2ndorder-head")
    add_p(
        "The primary contribution of this work is an empirical evaluation, rigorous uncertainty audit, and forensic failure analysis. "
        "The paper does not claim the invention of a novel standalone OOD algorithm or real-world agricultural supply chain deployment. "
        "The four specific, evidence-backed contributions of this study are:"
    )
    add_p(
        "1. Comprehensive Source-Stratified Benchmark Census (N = 13,465): We curate and publicly release an audited, leak-free evaluation "
        "benchmark comprising 13,465 image records structured across five distinct partitions: Partition A (Primary ID Test, N = 227), "
        "Partition B (External Known-Class Shift, N = 5,350), Partition C (Treatment-Labelled Condition Shift, N = 1,917), Partition D1 "
        "(Unseen-Species Shift, N = 4,776), and Partition D2 (Combined Shift, N = 1,195).",
        style="Els-numlist"
    )
    add_p(
        "2. Quantification of Closed-Set Domain Collapse: We demonstrate that the frozen MobileNetV2 backbone undergoes a severe 28.56 percentage-point "
        "drop in top-1 accuracy—collapsing from 96.92% [94.71%, 98.68%] on the laboratory test partition (Partition A) to 68.36% [67.20%, 69.40%] "
        "on pooled external retail fruit (Partition B). Through source-stratification, we show that performance varies significantly across external "
        "repositories (FruitVision: 69.14% accuracy, 69.56% balanced accuracy vs. Sultana: 65.63% accuracy, 65.55% balanced accuracy), with "
        "misclassifications heavily concentrated in russeted fresh apples and pale citrus cultivars.",
        style="Els-numlist"
    )
    add_p(
        "3. Source-Matched Isolation of Semantic vs. Treatment Shifts: By benchmarking within shared repositories, we eliminate cross-repository "
        "confounding. We demonstrate that while Energy-based detection achieves robust discrimination under Within-FruitVision semantic shift "
        "(Cohort A: 81.57% AUROC [80.81%, 82.38%], 13.18% operational UFAR), performance degrades significantly on external cultivars with visual "
        "overlap (Within-Sultana Cohort D: 67.52% AUROC [65.67%, 69.25%]).",
        style="Els-numlist"
    )
    add_p(
        "4. Empirical Diagnosis of Preservative Condition Failure & Operational Cost: We provide the first empirical evidence demonstrating that "
        "RGB image features alone cannot reliably distinguish formalin-treated produce from natural known fruit (Within-FruitVision Cohort B: "
        "Energy AUROC of only 53.13% [52.16%, 54.09%]). Under locked validation operating thresholds (tau95), 42.83% [41.26%, 44.34%] of "
        "treatment-labelled images are falsely accepted and classified as Fresh, conclusively demonstrating that surface vision cannot substitute "
        "for biochemical or multi-gas IoT sensing. Furthermore, we reveal that maintaining an operational UFAR of 16.07% on external produce "
        "requires accepting an in-distribution known-class abstention rate of approximately 41.98%.",
        style="Els-numlist"
    )

    # --- References Section ---
    add_p("References", style="Els-reference-head")

    references = [
        "[1] Food and Agriculture Organization (FAO), The State of Food and Agriculture 2019: Moving forward on food loss and waste reduction, Food and Agriculture Organization of the United Nations, Rome, 2019.",
        "[2] S. N. Jha, R. K. Vishwakarma, T. Ahmad, A. Rai, A. K. Dixit, Assessment of quantitative harvest and post-harvest losses of major crops and commodities in India, ICAR-All India Coordinated Research Project on Post-Harvest Technology, Ludhiana, 2015.",
        "[3] M. Rizzo, M. Marcuzzo, A. Zangari, A. Gasparetto, A. Albarelli, Fruit ripeness classification: A survey, Artificial Intelligence in Agriculture 7 (2023) 44–57. https://doi.org/10.1016/j.aiia.2023.02.004",
        "[4] Y. Zhang, X. Yang, Y. Cheng, X.-J. Wu, X. Sun, R. Hou, H. Wang, Fruit freshness detection based on multi-task convolutional neural network, Current Research in Food Science 8 (2024) 100733. https://doi.org/10.1016/j.crfs.2024.100733",
        "[5] H. Chen, G. Zhou, W. He, X. Duan, H. Jiang, Classification and identification of agricultural products based on improved MobileNetV2, Scientific Reports 14 (2024) 3214. https://doi.org/10.1038/s41598-024-53349-w",
        "[6] Y. Gulzar, Fruit Image Classification Model Based on MobileNetV2 with Deep Transfer Learning Technique, Sustainability 15 (3) (2023) 1906. https://doi.org/10.3390/su15031906",
        "[7] M. Sandler, A. Howard, M. Zhu, A. Zhmoginov, L.-C. Chen, MobileNetV2: Inverted Residuals and Linear Bottlenecks, in: Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR), 2018, pp. 4510–4520. https://doi.org/10.1109/CVPR.2018.00474",
        "[8] C. Guo, G. Pleiss, Y. Sun, K. Q. Weinberger, On Calibration of Modern Neural Networks, in: Proc. 34th Int. Conf. Mach. Learn. (ICML), PMLR 70, 2017, pp. 1321–1330.",
        "[9] D. Hendrycks, K. Gimpel, A Baseline for Detecting Misclassified and Out-of-Distribution Examples in Neural Networks, in: Proc. 5th Int. Conf. Learn. Represent. (ICLR), 2017.",
        "[10] W. J. Scheirer, A. de Rezende Rocha, R. J. Micheals, T. E. Boult, Toward Open Set Recognition, IEEE Trans. Pattern Anal. Mach. Intell. 35 (7) (2013) 1757–1772. https://doi.org/10.1109/TPAMI.2012.256",
        "[11] A. Bendale, T. E. Boult, Towards Open Set Deep Networks, in: Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR), 2016, pp. 1563–1572. https://doi.org/10.1109/CVPR.2016.173",
        "[12] J. Yang, K. Zhou, Y. Li, Z. Liu, Generalized Out-of-Distribution Detection: A Survey, International Journal of Computer Vision 132 (2024) 4619–4654. https://doi.org/10.1007/s11263-024-02117-4",
        "[13] S. Liang, Y. Li, R. Srikant, Enhancing The Reliability of Out-of-distribution Image Detection in Neural Networks, in: Proc. 6th Int. Conf. Learn. Represent. (ICLR), 2018.",
        "[14] K. Lee, K. Lee, H. Lee, J. Shin, A Simple Unified Framework for Detecting Out-of-Distribution Samples and Adversarial Attacks, in: Advances in Neural Information Processing Systems (NeurIPS), Vol. 31, 2018, pp. 7167–7177.",
        "[15] W. Liu, X. Wang, J. Owens, Y. Li, Energy-based Out-of-distribution Detection, in: Advances in Neural Information Processing Systems (NeurIPS), Vol. 33, 2020, pp. 21464–21475.",
        "[16] S. Vaze, K. Han, A. Vedaldi, A. Zisserman, Open-Set Recognition: A Good Closed-Set Classifier is All You Need, in: Proc. 10th Int. Conf. Learn. Represent. (ICLR), 2022.",
        "[17] O. Abayomi-Alli, R. Damaševičius, S. Misra, A. A. Abayomi-Alli, FruitQ: A new dataset of multiple fruit images for freshness evaluation, Multimedia Tools and Applications 82 (18) (2023) 27845–27871. https://doi.org/10.1007/s11042-023-16058-6",
        "[18] K. He, X. Zhang, S. Ren, J. Sun, Deep Residual Learning for Image Recognition, in: Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR), 2016, pp. 770–778. https://doi.org/10.1109/CVPR.2016.90",
        "[19] M. Tan, Q. V. Le, EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks, in: Proc. 36th Int. Conf. Mach. Learn. (ICML), PMLR 97, 2019, pp. 6105–6114.",
        "[20] R. R. Selvaraju, M. Cogswell, A. Das, R. Vedantam, D. Parikh, D. Batra, Grad-CAM: Visual Explanations from Deep Networks via Gradient-Based Localization, in: Proc. IEEE Int. Conf. Comput. Vis. (ICCV), 2017, pp. 618–626. https://doi.org/10.1109/ICCV.2017.74"
    ]

    for ref in references:
        add_p(ref, style="Els-reference")

    doc.save(str(OUTPUT_PATH))
    print(f"Successfully generated: {OUTPUT_PATH}")
    print(f"Total paragraphs in working manuscript: {len(doc.paragraphs)}")


if __name__ == "__main__":
    build_manuscript()

