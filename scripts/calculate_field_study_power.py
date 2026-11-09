#!/usr/bin/env python3
"""
scripts/calculate_field_study_power.py
======================================
Reproducible statistical power and sample size calculation for AgriRoute
observational prospective cohort field study.

Study Architecture:
- K = 40 shipments (clusters)
- m = 10 longitudinal tracked fruit specimens per shipment (N_tracked = 400)
- m_sac = 5 sacrificial baseline fruit specimens per shipment (N_sac = 200)
- Total planned collection = 600 fruit specimens

Calculates:
- Design effect (VIF) = 1 + (m - 1) * ICC
- Effective sample size N_eff = N_tracked / VIF
- Statistical power for detecting odds ratio (OR) across varying effect sizes,
  prevalence levels, and ICC values.
"""

import json
from pathlib import Path
import numpy as np
from scipy import stats

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def calculate_cluster_power(
    k_clusters: int = 40,
    m_per_cluster: int = 10,
    icc: float = 0.12,
    p0: float = 0.15,
    odds_ratio: float = 2.2,
    alpha: float = 0.05,
    attrition_rate: float = 0.05
):
    """
    Computes statistical power for clustered logistic regression.
    Follows Donner & Klar (2000) / Campbell et al. (2004) cluster trial formulation.
    """
    # Net tracked specimens after attrition
    n_nominal = k_clusters * m_per_cluster
    n_analyzable = n_nominal * (1.0 - attrition_rate)
    m_eff_cluster = m_per_cluster * (1.0 - attrition_rate)

    # Variance Inflation Factor
    vif = 1.0 + (m_eff_cluster - 1.0) * icc
    n_effective = n_analyzable / vif

    # Log odds formulation
    p1 = (p0 * odds_ratio) / (1.0 - p0 + p0 * odds_ratio)
    delta_p = p1 - p0
    p_bar = (p0 + p1) / 2.0

    # Z-critical value for two-sided alpha
    z_alpha = stats.norm.ppf(1.0 - alpha / 2.0)

    # Standard error under null and alternative
    # For binary comparison of high vs low risk exposure:
    # effective sample per group n_eff_group = n_effective / 2
    n_g = n_effective / 2.0
    se_null = np.sqrt(2.0 * p_bar * (1.0 - p_bar) / n_g)
    se_alt = np.sqrt((p0 * (1.0 - p0) + p1 * (1.0 - p1)) / n_g)

    # Z for power
    z_beta = (np.abs(delta_p) - z_alpha * se_null) / se_alt
    power = float(stats.norm.cdf(z_beta))

    return {
        "k_clusters": k_clusters,
        "m_per_cluster": m_per_cluster,
        "n_nominal": n_nominal,
        "attrition_rate": attrition_rate,
        "n_analyzable": n_analyzable,
        "icc": icc,
        "vif": float(vif),
        "n_effective": float(n_effective),
        "baseline_spoilage_p0": p0,
        "odds_ratio": odds_ratio,
        "elevated_spoilage_p1": float(p1),
        "delta_p": float(delta_p),
        "alpha": alpha,
        "power": power
    }

def main():
    print("Executing Clustered Field Study Power Analysis...")
    base_calc = calculate_cluster_power(k_clusters=40, m_per_cluster=10, icc=0.12, p0=0.15, odds_ratio=2.2)
    print(f"Base Configuration Power: {base_calc['power']*100:.2f}% (N_eff = {base_calc['n_effective']:.1f}, VIF = {base_calc['vif']:.2f})")

    # Sensitivity analysis across ICC (0.05 to 0.20) and OR (1.8 to 2.6)
    icc_range = [0.05, 0.08, 0.10, 0.12, 0.15, 0.20]
    or_range = [1.8, 2.0, 2.2, 2.4, 2.6]

    sensitivity = []
    for or_val in or_range:
        for icc_val in icc_range:
            res = calculate_cluster_power(k_clusters=40, m_per_cluster=10, icc=icc_val, p0=0.15, odds_ratio=or_val)
            sensitivity.append({
                "odds_ratio": or_val,
                "icc": icc_val,
                "vif": res["vif"],
                "n_effective": res["n_effective"],
                "power": res["power"]
            })

    output_data = {
        "study_design": "Observational Prospective Clustered Cohort",
        "cohort_breakdown": {
            "num_shipments_k": 40,
            "tracked_specimens_per_shipment_m": 10,
            "total_tracked_specimens": 400,
            "sacrificial_baseline_specimens_per_shipment": 5,
            "total_sacrificial_specimens": 200,
            "grand_total_specimens_collected": 600
        },
        "base_power_calculation": base_calc,
        "sensitivity_grid": sensitivity,
        "literature_sources_for_icc": [
            "Jedermann et al. (2014) - Spatial temperature and quality variation in container transports (Philosophical Transactions A)",
            "Defraeye et al. (2016) - Forced-convection cooling of citrus fruit (International Journal of Refrigeration)"
        ]
    }

    out_file = PROJECT_ROOT / "experiments" / "group_leakage_study" / "FIELD_STUDY_POWER_CALCULATION.json"
    with open(out_file, "w") as f:
        json.dump(output_data, f, indent=2)
    print(f"✅ Saved power calculation results to {out_file}")

if __name__ == "__main__":
    main()

