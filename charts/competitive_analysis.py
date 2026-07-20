"""Competitive analysis slide: Kaspi.kz vs fintech peers across key margin/return metrics."""

import matplotlib.pyplot as plt

from data.financials import COMPETITIVE_ANALYSIS


def plot(save_path="output/competitive_analysis.png"):
    df = COMPETITIVE_ANALYSIS

    ax = df.plot(kind="bar", figsize=(10, 6))
    ax.set_title("Kaspi.kz leads Fintech peers in key metrics", fontsize=9, fontweight="bold")
    ax.set_xlabel("Financial Metrics", fontsize=8)
    ax.set_ylabel("Percentage", fontsize=8)
    ax.tick_params(axis="x", labelsize=7, rotation=0)
    ax.tick_params(axis="y", labelsize=7)
    ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=7)
    ax.grid(True, axis="y")

    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(save_path, dpi=150)
    plt.close(fig)
    return save_path


if __name__ == "__main__":
    print(plot())
