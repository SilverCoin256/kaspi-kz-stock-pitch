"""Monte Carlo simulation: Kaspi.kz 10-year investment outlook.

Return-generating process: annual log-returns are i.i.d. Normal(mu, sigma),
so the cumulative multiple after t years is lognormal (standard GBM). Two
free parameters (mu, sigma) are solved in closed form from two of the deck's
target statistics, then every stat is re-derived (analytically and by actual
simulation) and compared against all five targets stated across the Risk /
Monte Carlo / Conclusion slides.

Note on an internal inconsistency in the source deck: for any unimodal
return distribution, P(X > threshold) <= 0.5 whenever threshold is above the
median. The deck states median = 3.2x over 10 years (=> median CAGR =
3.2**0.1 - 1 = 12.3%) AND separately "58% chance of exceeding 15% CAGR" --
but 15% > 12.3%, so at most ~50% of outcomes can exceed it, not 58%, under
any model calibrated to that median. Both numbers are reproduced as *targets*
below; the calibration matches median/positive-probability/loss-probability
exactly-to-closely and reports the CAGR>15% figure as structurally capped,
rather than silently forcing a fit.
"""

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import numpy as np
import matplotlib.pyplot as plt

from data.financials import MONTE_CARLO_TARGETS

MAJOR_LOSS_THRESHOLD = 0.5  # "major loss" := ending with <50% of starting capital


def _norm_cdf(x):
    """Standard normal CDF without a scipy dependency."""
    return 0.5 * (1.0 + np.vectorize(math.erf)(x / np.sqrt(2.0)))


def calibrate(targets=MONTE_CARLO_TARGETS):
    """Closed-form solve (mu, sigma) of annual log-returns from the median
    multiple and P(positive) targets, then evaluate every target analytically."""
    horizon = targets["horizon_years"]
    median_mult = targets["median_multiple"]

    mu = np.log(median_mult) / horizon

    z_pos = stats_ppf(targets["prob_positive"])
    sigma = mu * np.sqrt(horizon) / z_pos

    return {"mu": mu, "sigma": sigma, "horizon": horizon}


def stats_ppf(p):
    """Inverse standard normal CDF (percent-point function), no scipy needed."""
    # Acklam's algorithm (rational approximation), good to ~1e-9.
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]
    p_low = 0.02425
    if p < p_low:
        q = np.sqrt(-2 * np.log(p))
        return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
               ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    if p > 1 - p_low:
        q = np.sqrt(-2 * np.log(1 - p))
        return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
                ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    q = p - 0.5
    r = q * q
    return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / \
           (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)


def analytical_stats(mu, sigma, horizon):
    median_mult = np.exp(mu * horizon)
    mean_mult = np.exp(mu * horizon + 0.5 * sigma**2 * horizon)
    prob_positive = float(_norm_cdf(np.array([mu * np.sqrt(horizon) / sigma]))[0])
    prob_loss = 1 - prob_positive
    z_major = (np.log(MAJOR_LOSS_THRESHOLD) - mu * horizon) / (sigma * np.sqrt(horizon))
    prob_major_loss = float(_norm_cdf(np.array([z_major]))[0])
    z_cagr15_full = (np.log(1.15) - mu) / (sigma / np.sqrt(horizon))
    prob_cagr15_full_horizon = 1 - float(_norm_cdf(np.array([z_cagr15_full]))[0])
    z_cagr15_annual = (np.log(1.15) - mu) / sigma
    prob_cagr15_any_year = 1 - float(_norm_cdf(np.array([z_cagr15_annual]))[0])
    return {
        "median_multiple": median_mult,
        "mean_multiple": mean_mult,
        "prob_positive": prob_positive,
        "prob_loss": prob_loss,
        "prob_major_loss": prob_major_loss,
        "prob_cagr_above_15pct_full_horizon": prob_cagr15_full_horizon,
        "prob_cagr_above_15pct_any_single_year": prob_cagr15_any_year,
    }


def simulate(mu, sigma, horizon, n_sims, seed=7):
    """Return an (n_sims, horizon+1) array of cumulative-multiple paths."""
    rng = np.random.default_rng(seed)
    annual_log_returns = rng.normal(mu, sigma, size=(n_sims, horizon))
    cum_log = np.cumsum(annual_log_returns, axis=1)
    cum_log = np.hstack([np.zeros((n_sims, 1)), cum_log])
    return np.exp(cum_log)


def empirical_stats(paths):
    final = paths[:, -1]
    return {
        "median_multiple": float(np.median(final)),
        "mean_multiple": float(np.mean(final)),
        "prob_positive": float(np.mean(final > 1.0)),
        "prob_loss": float(np.mean(final < 1.0)),
        "prob_major_loss": float(np.mean(final < MAJOR_LOSS_THRESHOLD)),
    }


def plot_fan_chart(paths, save_path=None):
    save_path = Path(save_path) if save_path else ROOT / "output" / "monte_carlo.png"
    save_path.parent.mkdir(parents=True, exist_ok=True)
    years = np.arange(paths.shape[1])
    p10 = np.percentile(paths, 10, axis=0)
    p50 = np.percentile(paths, 50, axis=0)
    p90 = np.percentile(paths, 90, axis=0)
    mean = paths.mean(axis=0)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, p10, color="red", label="P10 (bear)")
    ax.plot(years, p50, color="green", label="Median")
    ax.plot(years, mean, color="black", linestyle="--", label="Mean")
    ax.plot(years, p90, color="cyan", label="P90 (bull)")

    ax.set_title(
        "Monte Carlo simulation: Kaspi.kz 10-year investment outlook\n"
        f"({paths.shape[0]:,} simulations | Kaspi.kz vs base case scenario)",
        fontsize=9, fontweight="bold",
    )
    ax.set_xlabel("Years", fontsize=8)
    ax.set_ylabel("Cumulative return multiple (x)", fontsize=8)
    ax.legend(loc="upper left", fontsize=7)
    ax.tick_params(labelsize=7)
    ax.grid(True, alpha=0.4)

    fig.tight_layout()
    fig.savefig(save_path, dpi=150)
    plt.close(fig)
    return str(save_path)


def run(targets=MONTE_CARLO_TARGETS, save_path=None):
    cal = calibrate(targets)
    mu, sigma, horizon = cal["mu"], cal["sigma"], cal["horizon"]

    paths = simulate(mu, sigma, horizon, targets["n_simulations"])
    a_stats = analytical_stats(mu, sigma, horizon)
    e_stats = empirical_stats(paths)
    out_path = plot_fan_chart(paths, save_path)

    report = {
        "calibrated_mu_annual": mu,
        "calibrated_sigma_annual": sigma,
        "analytical": a_stats,
        "empirical": e_stats,
        "targets": targets,
        "chart": out_path,
    }
    return report


if __name__ == "__main__":
    r = run()
    mu, sigma = r["calibrated_mu_annual"], r["calibrated_sigma_annual"]
    print(f"Calibrated annual log-return: mu={mu:.4f} sigma={sigma:.4f}\n")

    t = r["targets"]
    a = r["analytical"]
    e = r["empirical"]
    print(f"{'stat':38s} {'target':>10s} {'analytical':>12s} {'simulated':>12s}")
    print(f"{'median multiple':38s} {t['median_multiple']:>10.2f} {a['median_multiple']:>12.2f} {e['median_multiple']:>12.2f}")
    print(f"{'P(positive return)':38s} {t['prob_positive']:>10.1%} {a['prob_positive']:>12.1%} {e['prob_positive']:>12.1%}")
    print(f"{'P(loss)':38s} {t['prob_loss']:>10.1%} {a['prob_loss']:>12.1%} {e['prob_loss']:>12.1%}")
    print(f"{'P(major loss, <0.5x)':38s} {t['prob_major_loss']:>10.1%} {a['prob_major_loss']:>12.1%} {e['prob_major_loss']:>12.1%}")
    print(f"{'P(CAGR>15%, full 10yr horizon)':38s} {t['prob_cagr_above_15pct']:>10.1%} {a['prob_cagr_above_15pct_full_horizon']:>12.1%} {'--':>12s}")
    print(f"{'P(CAGR>15%, any single year)':38s} {'--':>10s} {a['prob_cagr_above_15pct_any_single_year']:>12.1%} {'--':>12s}")
    print(
        "\nNote: median-3.2x and '58% exceed 15% CAGR' cannot both hold exactly "
        "(15% CAGR is above the 12.3% median-implied CAGR, which caps any "
        "exceedance probability at ~50%). See module docstring."
    )
    print(f"\nChart saved to {r['chart']}")
