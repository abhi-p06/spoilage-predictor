---
name: systematic-literature-search
description: Execute reproducible, multi-database scholarly literature searches across OpenAlex, Semantic Scholar, Scite, and arXiv to benchmark modern post-harvest vision and routing systems.
---

# Objective
Perform structured, reproducible bibliographic searches across scientific repositories to locate seminal, state-of-the-art, and recent (2020–2026) peer-reviewed papers on fruit quality computer vision, cold-chain IoT tracking, dynamic perishable routing, and multi-sensor fusion.

# Workflow

1. **Formulate Query Strings:**
   - Define boolean search strings targeting core research facets:
     - *Facet 1 (Vision Quality):* `("fruit quality" OR "post-harvest spoilage" OR "defect detection") AND ("deep learning" OR "MobileNet" OR "EfficientNet" OR "ResNet" OR "transfer learning")`
     - *Facet 2 (Cold-chain IoT):* `("cold chain" OR "spoilage prediction" OR "perishability") AND ("IoT" OR "environmental sensors" OR "temperature abuse" OR "LSTM")`
     - *Facet 3 (Perishable Logistics):* `("dynamic routing" OR "vehicle routing" OR "VRPTW") AND ("perishable" OR "fresh produce" OR "spoilage risk")`
     - *Facet 4 (Multi-Modal Fusion):* `("multimodal" OR "multi-sensor fusion" OR "sensor vision") AND ("agriculture" OR "fruit")`
2. **Execute Across Scholarly APIs:**
   - Query configured endpoints (OpenAlex, Semantic Scholar, Scite, arXiv).
   - Log exact search query, API endpoint, date of query, and returned record count.
3. **Screen and Filter Results:**
   - Filter by year (prioritize 2022–2026 for SOTA comparison; include pre-2022 only for seminal foundational algorithms).
   - Require peer-reviewed status (Q1/Q2 journals like *Computers and Electronics in Agriculture*, *Postharvest Biology and Technology*, *IEEE T-ASE*, *Journal of Food Engineering*, or established IEEE/ACM conferences).
4. **Extract Key Comparative Attributes:**
   - Architecture / Backbone (e.g., MobileNetV2, YOLO, ResNet, BiLSTM).
   - Dataset & Modality (sample size, laboratory vs. field capture, sensor types).
   - Evaluation Metrics (Accuracy, F1, AUC, ECE, computational latency).
   - Routing Integration (static vs. dynamic, objective formulation).
   - Real-World Deployment Validation ($N$ field runs vs. simulation).
5. **Update Reference Repository:**
   - Export BibTeX entries to the reference library index.
   - Record candidate papers in `research_memory/reference_library_index.md`.

