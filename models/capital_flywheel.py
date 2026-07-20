"""Capital Flywheel slide: self-funded growth via high-ROIC reinvestment.

Deterministic compounding model — each series is base_value * (1 + rate) ** t.
Not a simulation: reproducing it is just re-running the same compounding math
with the rates stated in the deck's own legend (Revenue 15%, Earning Power 18%,
Reinvestment 22%).
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import matplotlib.pyplot as plt
import pandas as pd

from data.financials import FLYWHEEL_ASSUMPTIONS

COLORS = {"Revenue (15%)": "red", "Earning Power (18%)": "blue", "Reinvestment (22%)": "green"}


def build_table():
    base = FLYWHEEL_ASSUMPTIONS["base_value"]
    years = range(FLYWHEEL_ASSUMPTIONS["years"] + 1)
    data = {name: [base * (1 + rate) ** t for t in years] for name, rate in FLYWHEEL_ASSUMPTIONS["series"].items()}
    return pd.DataFrame(data, index=list(years))


def plot(save_path=None):
    save_path = Path(save_path) if save_path else ROOT / "output" / "capital_flywheel.png"
    save_path.parent.mkdir(parents=True, exist_ok=True)
    df = build_table()

    fig, ax = plt.subplots(figsize=(10, 6))
    for name in df.columns:
        ax.plot(df.index, df[name], marker="o", color=COLORS[name], label=name)

    ax.set_title(
        "Kaspi.kz Capital Flywheel: Self-funded Growth via High-ROIC Reinvestment\n"
        "Capital quality (ROIC 18-22%) drives 18-22% earnings growth through reinvestment cycles",
        fontsize=8, fontweight="bold",
    )
    ax.set_xlabel("Years / Reinvestment cycles", fontsize=8)
    ax.set_ylabel("KZT Bln", fontsize=8)
    ax.legend(loc="upper left", fontsize=7)
    ax.tick_params(labelsize=7)

    fig.tight_layout()
    fig.savefig(save_path, dpi=150)
    plt.close(fig)
    return str(save_path)


if __name__ == "__main__":
    print(build_table().round(0))
    print(plot())
