"""Revenue Growth slide: Kaspi.kz Total Revenue and Net Income, 2020-2024 (KZT Bln)."""

import matplotlib.pyplot as plt

from data.financials import REVENUE_GROWTH


def plot(save_path="output/revenue_growth.png"):
    df = REVENUE_GROWTH

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df["Year"], df["Total Revenue"], marker="o", label="Total Revenue")
    ax.plot(df["Year"], df["Net Income"], marker="o", color="green", label="Net Income")

    ax.set_title("Kaspi.kz Revenue and Net Income Rising (2020-2024)", fontsize=9, fontweight="bold")
    ax.set_xlabel("Year", fontsize=8)
    ax.grid(True)
    ax.legend(loc="upper left", fontsize=7)
    ax.tick_params(labelsize=7)

    fig.tight_layout()
    fig.savefig(save_path, dpi=150)
    plt.close(fig)
    return save_path


if __name__ == "__main__":
    print(plot())
