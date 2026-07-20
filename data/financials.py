"""
Kaspi.kz (NASDAQ: KSPI) historical financials and peer comparables.

Figures hand-collected from Kaspi.kz investor-relations filings (20-F, quarterly
results, prospectus) and third-party aggregators (stockanalysis.com, Yahoo Finance,
GuruFocus) — see README.md > Data Sources for the full reference list.
"""

import pandas as pd

# ---------------------------------------------------------------------------
# Revenue Growth chart (Total Revenue vs Net Income, KZT Billions, 2020-2024)
# ---------------------------------------------------------------------------
REVENUE_GROWTH = pd.DataFrame({
    "Year": [2020, 2021, 2022, 2023, 2024],
    "Total Revenue": [600, 880, 1260, 1875, 2505],
    "Net Income": [260, 430, 580, 830, 1030],
})

# ---------------------------------------------------------------------------
# Net income metrics, USD Billions, 2020-2024
# ---------------------------------------------------------------------------
NET_INCOME_METRICS = pd.DataFrame(
    {
        2020: [3, 1, 2, 61.3, 71.5],
        2021: [5, 2, 3, 62.9, 78.1],
        2022: [7, 5, 5, 75.7, 78.7],
        2023: [10, 7, 9, 78.0, 78.3],
        2024: [14, 10, 11, 83.2, 75.1],
    },
    index=["Total Revenue", "Operating Income", "Net Income", "Operating Margin %", "Net Profit Margin %"],
)

# ---------------------------------------------------------------------------
# Cash flow metrics, USD Millions, 2020-2024
# ---------------------------------------------------------------------------
CASH_FLOW_METRICS = pd.DataFrame(
    {
        2020: [711_000_000, 562_000_000, 65, 39, None],
        2021: [1_051_000_000, 895_000_000, 62, 43, None],
        2022: [1_310_000_000, 1_094_000_000, 70, 35, None],
        2023: [1_802_000_000, 1_482_000_000, 66, 32, 4.2],
        2024: [1_418_000_000, 1_180_000_000, 67, 19, 8.8],
    },
    index=["Operating Cash Flow", "Free Cash Flow", "Return on Equity %", "FCF Margin %", "FCF Yield %"],
)

# ---------------------------------------------------------------------------
# Comparable company multiples (valuation slide)
# ---------------------------------------------------------------------------
COMPS_MULTIPLES = pd.DataFrame(
    [
        {"Company": "Kaspi.kz",     "P/E": 6.1,  "PEG Ratio": 0.24, "ROE": 68.5, "Net Margin": 41.0},
        {"Company": "MercadoLibre", "P/E": 52.4, "PEG Ratio": 1.53, "ROE": 42.0, "Net Margin": 7.7},
        {"Company": "Sea Limited",  "P/E": 25.8, "PEG Ratio": 0.74, "ROE": 15.3, "Net Margin": 6.3},
        {"Company": "PayPal",       "P/E": 10.5, "PEG Ratio": 3.40, "ROE": 25.0, "Net Margin": 15.6},
        {"Company": "Grab",         "P/E": 50.3, "PEG Ratio": 2.24, "ROE": None, "Net Margin": None},
    ]
).set_index("Company")

# ---------------------------------------------------------------------------
# Competitive analysis of financials (grouped bar chart), % of revenue/equity
# ---------------------------------------------------------------------------
COMPETITIVE_ANALYSIS = pd.DataFrame(
    {
        "Kaspi.kz":      [48, 52, 80, 9, 34],
        "PayPal":        [15, 18, 20, 8, 12],
        "Block":         [2, 8, 0, 4, 2],
        "MercadoLibre":  [6, 12, 15, 3, 8],
        "Nu Holdings":   [8, 15, 28, 5, 10],
    },
    index=["Net Profit %", "Operating %", "ROE %", "FCF Yield %", "FCF Marg %"],
)

# ---------------------------------------------------------------------------
# Investment recommendation / trading snapshot
# ---------------------------------------------------------------------------
TRADING_SNAPSHOT = {
    "recommendation": "Strong Buy",
    "current_price": 76.50,       # used on valuation + conclusion slides
    "current_price_asof": 76.30,  # slide 2, as of 2026-02-02
    "price_target": 140.0,
    "target_horizon_months": (12, 18),
    "market_cap": 14.6e9,
    "week52_low": 70.61,
    "week52_high": 111.45,
    "shares_outstanding": 199.5e6,
    "avg_daily_volume_shares": 479_000,
    "float_shares": 76.5e6,
}

# ---------------------------------------------------------------------------
# Valuation scenarios
# ---------------------------------------------------------------------------
VALUATION_SCENARIOS = pd.DataFrame(
    [
        {"Scenario": "Best Case",  "Chance": 0.30, "Drivers": "Massive success in Turkey leading to 30%+ growth", "Target Price": 175.0},
        {"Scenario": "Base Case",  "Chance": 0.55, "Drivers": "Steady growth of 25%",                              "Target Price": 140.0},
        {"Scenario": "Worst Case", "Chance": 0.15, "Drivers": "Slow growth of around 15%",                         "Target Price": 100.0},
    ]
).set_index("Scenario")

# ---------------------------------------------------------------------------
# Capital flywheel reinvestment model assumptions
# ---------------------------------------------------------------------------
FLYWHEEL_ASSUMPTIONS = {
    "base_value": 1000,  # KZT Bln, indexed to year 0
    "years": 5,
    "series": {
        "Revenue (15%)":       0.15,
        "Earning Power (18%)": 0.18,
        "Reinvestment (22%)":  0.22,
    },
}

# ---------------------------------------------------------------------------
# Monte Carlo target statistics (as stated across the Risk / Monte Carlo /
# Conclusion slides) — the calibration routine in models/monte_carlo.py tries
# to reproduce these as closely as jointly possible.
# ---------------------------------------------------------------------------
MONTE_CARLO_TARGETS = {
    "n_simulations": 1000,
    "horizon_years": 10,
    "median_multiple": 3.2,
    "prob_positive": 0.89,
    "prob_cagr_above_15pct": 0.58,
    "prob_loss": 0.10,
    "prob_major_loss": 0.03,
}

# ---------------------------------------------------------------------------
# Risk & stress test figures (Risk and Stress Tests slide)
# ---------------------------------------------------------------------------
RISK_STRESS = {
    "forward_pe": 6.2,
    "peer_discount_pct": 78,
    "bear_case_prob": 0.05,
    "bear_case_price": 54.0,
    "roe_decay_from": 68.0,
    "roe_decay_to": 40.0,
    "roe_decay_fair_value": 162.0,
    "severe_margin_drop_pct": 10,
    "eps_impact_from_margin_drop_pct": -27,
    "gdp_correlation": -0.16,
    "npl_stressed_pct": 9.0,
    "npl_margin_impact_pct": -3.6,
    "var95_max_drawdown_pct": 41,
    "avg_daily_dollar_volume": 36e6,
}

# ---------------------------------------------------------------------------
# Key operating metrics dashboard
# ---------------------------------------------------------------------------
OPERATING_METRICS = {
    "txns_per_user_days": 1.3,
    "cac_decline_since_2020_pct": 60,
    "ltv_usd": 285,
    "npl_ratio_pct": 2.8,
    "loan_approval_seconds": 60,
    "payments_market_share_pct": 78,
    "adult_population_penetration_pct": 75,
    "monthly_active_users": 15e6,
}
