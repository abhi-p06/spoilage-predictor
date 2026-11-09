---
name: literature-matrix
description: Build a verified state-of-the-art literature review and a feature-based comparison of AgriRoute with post-harvest decision systems and agri-logistics platforms.
---

# Objective

Find the actual research gap and determine whether AgriRoute contributes more than integrating existing components. Do not begin by assuming novelty.

# Search themes

Search peer-reviewed work on: fruit freshness/quality computer vision; post-harvest loss and shelf-life estimation; multimodal sensor/image fusion; cold-chain monitoring; perishability-aware vehicle routing; quality-aware routing; agricultural logistics decision support; market-aware distribution; and comparable agri-logistics platforms.

# Source workflow

1. Search broadly using Exa or another connected research/search MCP. Use OpenAlex and Crossref to discover and verify bibliographic metadata.
2. For every selected paper, open the publisher or DOI landing page. Verify the title, complete author list, venue, year, DOI, task, dataset, model, validation setting, and reported metric.
3. Prefer peer-reviewed primary studies for technical claims. Use official product/platform documentation for product features. Clearly label product/vendor claims and do not treat them as peer-reviewed performance evidence.
4. Do not cite a result based only on an abstract or search snippet where the method/results are central. Retrieve the full paper or a reliable author/publisher version when possible.
5. Check whether a paper is a preprint, conference paper, journal article, dataset paper, or vendor white paper. Do not conflate them.
6. Record the date the source was accessed and any access limitations. If an exact detail cannot be confirmed, mark it `UNVERIFIED` and do not write it as fact.

# Required outputs

Create a literature matrix with columns:
`Citation | DOI/URL | Source type | Problem | Data/fruit | Method | Validation protocol | Metrics | Limitations | Feature relevant to AgriRoute | Evidence confidence`.

Create a separate platform comparison table with columns:
`System/platform | Primary purpose | Freshness/quality vision | Cold-chain/sensor monitoring | Route optimization | Market/demand integration | Shipment-level traceability | Publicly documented evidence | Source/date`.

Include AgriRoute as the proposed system, but mark every feature as `implemented`, `prototype`, `planned`, or `not demonstrated` based on repository evidence. Do not fill missing features with assumptions.

# Novelty analysis

Identify the closest 5–10 studies/systems, then state:
- what each already does;
- what AgriRoute does differently (if anything demonstrable);
- what experiment would test that difference;
- whether the difference is methodological, empirical, or only an implementation/integration contribution.

If no defensible methodological novelty is present, say so clearly and recommend a narrower, honest contribution rather than inventing novelty.
