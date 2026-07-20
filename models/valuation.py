"""Valuation, comps, and risk-stress outputs (Valuation / Comps / Risk slides).

Reports the deck's stated figures, plus every cross-check that reproduces one
stated number from two others (useful as a provenance check on the hardcoded
data in data/financials.py -- if these stop tying out, the input data is
probably wrong, not the arithmetic).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from data.financials import (
    TRADING_SNAPSHOT,
    VALUATION_SCENARIOS,
    COMPS_MULTIPLES,
    COMPETITIVE_ANALYSIS,
    RISK_STRESS,
    OPERATING_METRICS,
)


def price_target_upside(current=None, target=None):
    if current is None:
        current = TRADING_SNAPSHOT["current_price"]
    if target is None:
        target = TRADING_SNAPSHOT["price_target"]
    return target / current - 1


def probability_weighted_target():
    df = VALUATION_SCENARIOS
    return float((df["Chance"] * df["Target Price"]).sum())


def peer_average(column, exclude="Kaspi.kz"):
    s = COMPS_MULTIPLES[column].drop(index=exclude)
    return float(s.dropna().mean())


def discount_to_peers(column="P/E"):
    kaspi = COMPS_MULTIPLES.loc["Kaspi.kz", column]
    return 1 - kaspi / peer_average(column)


def earnings_yield():
    return 1 / COMPS_MULTIPLES.loc["Kaspi.kz", "P/E"]


def margin_multiple_vs_mercadolibre(metric="Operating %"):
    return COMPETITIVE_ANALYSIS.loc[metric, "Kaspi.kz"] / COMPETITIVE_ANALYSIS.loc[metric, "MercadoLibre"]


def roe_decay_upside():
    return RISK_STRESS["roe_decay_fair_value"] / TRADING_SNAPSHOT["current_price"] - 1


def npl_sensitivity_ratio():
    delta_npl = RISK_STRESS["npl_stressed_pct"] - OPERATING_METRICS["npl_ratio_pct"]
    return RISK_STRESS["npl_margin_impact_pct"] / delta_npl


def eps_operating_leverage_factor():
    return RISK_STRESS["eps_impact_from_margin_drop_pct"] / -RISK_STRESS["severe_margin_drop_pct"]


def run():
    print("=== Valuation & Price Target ===")
    print(f"Current price: ${TRADING_SNAPSHOT['current_price']:.2f}")
    print(f"Price target:  ${TRADING_SNAPSHOT['price_target']:.2f}")
    print(f"Upside:        {price_target_upside():.1%}")
    print(f"Probability-weighted scenario target: ${probability_weighted_target():.2f}")
    print()
    print(VALUATION_SCENARIOS)

    print("\n=== Comparable Company Multiples ===")
    print(COMPS_MULTIPLES)
    print(f"\nKaspi P/E discount to peer average:  {discount_to_peers('P/E'):.1%}")
    print(f"Kaspi PEG discount to peer average:  {discount_to_peers('PEG Ratio'):.1%}")
    print(f"Kaspi earnings yield (1 / P/E):       {earnings_yield():.1%}")
    print(f"Kaspi vs MercadoLibre operating-margin multiple: {margin_multiple_vs_mercadolibre():.1f}x")

    print("\n=== Risk & Stress Tests ===")
    print(RISK_STRESS)
    print(f"\nUpside at decayed-ROE fair value floor ($162): {roe_decay_upside():.1%}")
    print(f"Implied NPL-stress margin sensitivity: {npl_sensitivity_ratio():.2f} margin-pp per NPL-pp")
    print(f"Implied EPS operating-leverage factor: {eps_operating_leverage_factor():.2f}x margin move")


if __name__ == "__main__":
    run()
