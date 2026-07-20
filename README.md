# Kaspi.kz Stock Pitch — Ascend Berkeley Stock Pitch Competition 2025

Rebuilt analysis code behind *"Kaspi.kz: A Compelling Case for Fintech Leadership"*
(Prajwal Doranala & Shaurya Santosh Gupta). The original code was lost; this
repo reconstructs it from the submitted deck — historical financials, comps,
the Monte Carlo simulation, and the capital-flywheel reinvestment model — so
every chart and figure in the deck can be regenerated and re-verified.

**Recommendation: Strong Buy** · Current price $76.50 · 12-18mo target $140 (+83%)

## Run it

```bash
pip install -r requirements.txt
python run_all.py
```

Charts land in `output/`; every table and stat prints to stdout.

## Layout

- `data/financials.py` — hardcoded historical financials, peer comps, valuation scenarios, risk-test inputs. Every number is footnoted to the slide it feeds.
- `charts/revenue_growth.py` — Total Revenue / Net Income, 2020-2024 (KZT Bln) line chart.
- `charts/competitive_analysis.py` — grouped bar chart, Kaspi vs. PayPal / Block / MercadoLibre / Nu Holdings across 5 profitability metrics.
- `models/capital_flywheel.py` — deterministic reinvestment-compounding model (Revenue 15% / Earning Power 18% / Reinvestment 22%).
- `models/monte_carlo.py` — 1,000-path, 10-year GBM-style simulation, closed-form calibrated to the deck's target stats, with an analytical-vs-simulated verification pass.
- `models/valuation.py` — scenario-weighted price target, comps discount math, risk-stress sensitivities, and cross-checks that re-derive one stated figure from two others.
- `run_all.py` — runs everything end to end.

## Data sources

Pulled from Kaspi.kz investor relations, SEC filings, and the third-party
aggregators listed on the deck's References slides:

- ir.kaspi.kz — financial results (1Q/2Q/3Q/4Q 2025, FY2024), 20-F filings (2023, 2024), prospectus, registration document, 2023 ESG report, ecosystem/marketplace pages
- SEC EDGAR — kspi-20241231.htm, kspi-20231231.htm, kspi-ex99_1.htm (CIK 1985487)
- finance.yahoo.com/quote/KSPI — financials, key statistics, price history
- stockanalysis.com, companiesmarketcap.com, statista.com, gurufocus.com — revenue/margin/FCF-yield cross-checks
- koalagains.com, videttecapitalresearch.substack.com, schwarcapital.com, nextgeninvestors.substack.com, beyondspx.com, alphaspread.com, portersfiveforce.com — qualitative/competitive research
- nationalbank.kz, investing.com — USD/KZT exchange rates
- iclg.com — Kazakhstan digital business regulation

## Known data caveats

Reconstructed from a rendered PDF, not the original spreadsheets, so two
things are worth flagging rather than silently smoothing over:

1. **"Net income metrics in million USD" (slide 18) is almost certainly USD
   billions**, not millions — the values (Revenue $3→$14) only make sense at
   Kaspi's actual scale as billions, and the deck's own Revenue Growth chart
   (slide 13, KZT bn) implies a similar order of magnitude once converted.
   Reproduced verbatim as labeled in `data/financials.py`.
2. **The Monte Carlo target stats are mutually inconsistent.** The deck
   states both "median = 3.2x over 10 years" (implies median CAGR ≈ 12.3%)
   and "58% chance of exceeding 15% CAGR" — but 15% is *above* the
   12.3%-implied median, which caps any exceedance probability at ~50% under
   any unimodal return model. `models/monte_carlo.py` calibrates to the
   median/positive-probability/loss-probability targets (which are mutually
   consistent) and reports the 15%-CAGR figure candidly as structurally
   capped rather than forcing a fit — see the module docstring.

Two independent peer sets appear in the deck and are kept separate rather
than merged: the comps table (`COMPS_MULTIPLES`: Kaspi, MercadoLibre, Sea
Limited, PayPal, Grab — P/E, PEG, ROE, Net Margin) and the competitive-bar-chart
set (`COMPETITIVE_ANALYSIS`: Kaspi, PayPal, Block, MercadoLibre, Nu Holdings —
Net Profit / Operating / ROE / FCF Yield / FCF Margin %). Several bullet
points in the deck cross-check cleanly against this data (Kaspi's PEG
discount to peers ≈87%, earnings yield ≈16%, ROE-decay fair-value upside
≈112%) — `models/valuation.py` reproduces and prints those checks.

## Disclaimer

Built for an academic stock-pitch competition. Not investment advice.
