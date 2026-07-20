"""Generate every chart and printed table used in the Kaspi.kz stock pitch deck."""

import os

from data.financials import NET_INCOME_METRICS, CASH_FLOW_METRICS, TRADING_SNAPSHOT
from charts import revenue_growth, competitive_analysis
from models import capital_flywheel, monte_carlo, valuation


def main():
    os.makedirs("output", exist_ok=True)

    print("=== Investment Recommendation ===")
    print(TRADING_SNAPSHOT)

    print("\n=== Revenue Growth chart ===")
    print(revenue_growth.plot())

    print("\n=== Net income metrics ===")
    print(NET_INCOME_METRICS)

    print("\n=== Cash flow metrics ===")
    print(CASH_FLOW_METRICS)

    print("\n=== Competitive analysis chart ===")
    print(competitive_analysis.plot())

    print("\n=== Capital flywheel model ===")
    print(capital_flywheel.build_table().round(0))
    print(capital_flywheel.plot())

    print("\n=== Monte Carlo simulation ===")
    mc = monte_carlo.run()
    print(f"chart: {mc['chart']}")
    print(f"analytical stats: {mc['analytical']}")
    print(f"empirical stats:  {mc['empirical']}")

    print()
    valuation.run()


if __name__ == "__main__":
    main()
