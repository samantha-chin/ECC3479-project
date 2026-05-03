# visualisations README

This document is specific to [visualisations.ipynb](visualisations.ipynb) and is intentionally separate from the main project README for [ECC3479_notebook.ipynb](ECC3479_notebook.ipynb).

## overview

This notebook explores whether suburbs near the Upfield line (affected by level crossing removals) exhibit faster house price growth than more distant suburbs.

The analysis provides descriptive and visual evidence to guide later causal modelling.

## Research Question

Will the removal of level crossings and related transport improvements along the Upfield line drive faster house price growth in adjacent suburbs compared to those located away from the line?

## Scope of visualisations

The exploratory analysis focuses on three main variables:

- Suburb
- House price
- Population density

The notebook compares adjacent suburbs and faraway suburbs over time to check whether their price-growth paths differ.

Suburbs are classified as:
- **Adjacent**: near Upfield line / LXRP sites
- **Faraway**: not directly affected

## What visualisations.ipynb Does

### Data Preparation
- Loads cleaned suburb-level datasets from `data/clean`
- Merges house prices, density, proximity, and income into a panel dataset

### Feature Construction
- Classifies suburbs into adjacent vs faraway groups
- Structures data for time-series and panel comparisons

### Visual Analysis

Generates:
- Ranked suburb median house prices
- Boxplots comparing adjacent vs faraway suburbs
- Population density distributions
- Time trends for prices and density
- Scatter plots and correlation analysis

### Diagnostics
- Between vs within suburb variation
- OLS residual diagnostics

Each graph includes a written interpretation linked to the research question.

## Key Data Used

Typical files referenced in `data/clean` include:

- `adjacent_suburbs_house_prices_2015_2024.csv`
- `faraway_suburbs_house_prices_2015_2024.csv`
- `closest_lxrp_site_house_prices_2015_2024.csv`
- `requested_suburbs_density_2015_2024.csv`
- `requested_suburbs_density_2015_2024_long.csv`
- `annual_household_income_table.csv`

## How To Run visualisations

1. Open [visualisations.ipynb](visualisations.ipynb) in VS Code or Jupyter.
2. Install dependencies (or use the project virtual environment):

```bash
pip install pandas numpy matplotlib seaborn openpyxl jupyter
```

3. Run cells from top to bottom so shared setup variables are available to later graph cells.
4. Review charts and their paired markdown interpretations directly below each graph.

## Interpretation Notes

- Pearson correlation is useful as a supporting descriptive metric, but it is not the core evidence for the research question.
- The strongest evidence in this notebook comes from adjacent-vs-faraway trend comparisons and panel-aware checks (between vs within variation).
- Use EDA findings as directional evidence before any formal causal modelling.

- Distances for suburbs to the closest LXRP site were manually entered from Google Maps.
- To ensure fairness, each distance was measured from the middle of the chosen suburb to the closest LXRP site.
- Some values in the grouped suburb house price tables were manually typed in because the raw file contained messy tables that the code could not reliably parse.