# Primary Econometric Analysis README

This document describes the purpose, inputs, outputs, and how-to-run instructions for `primary econometric analysis.ipynb`.

## Overview

`primary econometric analysis.ipynb` contains the main econometric modelling and estimation steps that follow the exploratory analysis in `visualisations.ipynb` and the data cleaning in `ECC3479_notebook.ipynb`.

The notebook implements a difference-in-differences design to estimate whether early LXRP construction or completions by 2017 changed house prices in treated suburbs relative to LXRP-listed suburbs not yet exposed.

## Purpose

- Estimate the primary difference-in-differences specification around the 2017 exposure cutoff.
- Produce model tables, diagnostic plots, and a short set of robustness checks.
- Save regression outputs and key tables for reporting.

## Scope and Key Analyses

- Difference-in-differences (DiD) specification using early exposure by 2017
- Models with time effects and time-varying controls (e.g., log population)
- Robustness checks (alternative exposure definitions and functional forms)

## Key Data Used

Inputs are expected to be present in `data/clean/`, typically produced by `ECC3479_notebook.ipynb` and related scripts:

- `suburbs_house_prices_2015_2024_wide_complete.csv` — cleaned house prices (wide format)
- `requested_suburbs_density_2015_2024_long.csv` — population density (long format)
- `daniel_bowen_treated_suburbs_2022.csv` — early-exposed suburb list
- `daniel_bowen_untreated_suburbs_2022.csv` — not-yet-exposed suburb list

If any of these files are missing, run `ECC3479_notebook.ipynb` first to regenerate cleaned data.

## Typical Outputs

- Regression tables and coefficient CSVs saved under `outputs/econometrics/` (CSV and `.pkl` formats)
- Diagnostic plots (residuals, leverage, fitted vs observed) in `outputs/econometrics/figures/`
- A short summary table with estimated treatment effects and standard errors

## How To Run

1. Open `primary econometric analysis.ipynb` in VS Code or Jupyter.
2. Ensure the project's Python environment has required packages:

```bash
pip install pandas numpy statsmodels linearmodels matplotlib seaborn jupyter
```

3. Run the notebook cells from top to bottom. The notebook assumes the cleaned `data/clean` CSVs are available and that the shared setup cell defines early-exposed and not-yet-exposed suburb lists used to build `Exposed` and `Post2017` indicators.
4. Inspect and save outputs in `outputs/econometrics/`.

## Recommended Workflow

- Run `ECC3479_notebook.ipynb` first to ensure cleaned inputs are present in `data/clean/`.
- Run `visualisations.ipynb` for EDA and to confirm sample definitions and functional forms.
- Then run `primary econometric analysis.ipynb` to estimate models and produce result artifacts.

## Notes and Assumptions

- Suburb name standardization (title case, stripped whitespace) is assumed; mismatches can cause joins to drop observations.
- Price variables in the notebook are typically logged (`log_price`)—check the shared setup cell for the exact variable name.
- Population density coverage may be incomplete for some suburbs; if density-based controls are used, confirm the sample and merging strategy to avoid dropping not-yet-exposed suburbs unintentionally.
- Regression code uses `statsmodels` and (optionally) `linearmodels` for panel estimators.


