# Robustness Table Notebook

## Overview

`Robustness Table.ipynb` builds robustness checks for the difference-in-differences
analysis of house prices. The notebook checks whether the main estimated treatment
effect is stable when the model specification changes.

The main estimate is the `Treat x Post` coefficient. This is the DiD treatment
effect: it compares the change in prices for treated suburbs after the treatment
period (starting in 2017) with the change in prices for control suburbs.

The notebook includes:

- A baseline DiD model.
- Alternative functional-form checks.
- A 2017 milestone pre-trend test.
- A joint pre-trend test.
- A final formatted robustness table.

The results show that the Treat x Post coefficient is small and statistically
insignificant across all specifications, indicating no clear post-2017 price
effect in treated suburbs relative to controls.

## Files Included

### Main notebook

- `Robustness Table.ipynb`

  Runs the robustness checks and displays the robustness table.

### Supporting code

- `code/robustness_analysis.py`

  Builds the cleaned panel dataset used in the regressions and provides helper
  functions such as significance stars.

- `code/robustness_functional_form.py`

  Contains earlier functional-form robustness models used by some cells in the
  notebook.

- `code/robustness_pretrend_test.py`

  Contains earlier pre-trend test logic and output helpers.

### Output files

Some robustness results are also saved in the `results/` folder:

- `results/robustness_functional_form.csv`
- `results/robustness_functional_form.md`
- `results/robustness_functional_form.html`
- `results/robustness_pretrend_test_2017_milestone.csv`
- `results/robustness_pretrend_test_2017_milestone.md`
- `results/robustness_pretrend_test_2017_milestone.html`
- `results/robustness_combined_side_by_side.csv`
- `results/robustness_combined_side_by_side.md`
- `results/robustness_combined_side_by_side.html`

The notebook itself displays the table directly, so these files are useful if
you want to copy results into a report or inspect saved outputs separately.

## Packages Used

The notebook uses the following Python packages:

- `pathlib`
- `sys`
- `numpy`
- `pandas`
- `statsmodels`

The main statistical package is `statsmodels`, which estimates the OLS
regressions and calculates robust standard errors.

## How To Run The Notebook

1. Open `Robustness Table.ipynb` in Jupyter Notebook, JupyterLab, or VS Code.
2. Make sure the project root is the working directory.
3. Run the notebook cells from top to bottom.
4. The final robustness table will appear as a pandas table output.

The notebook imports helper code from the `code/` folder, so it should be run
from the project root directory rather than from inside the `code/` folder.

## Models Estimated

### Baseline

The baseline model estimates:

```text
log_price ~ treat_post + log_population + suburb fixed effects + year fixed effects
```

This is the main DiD specification, where `treat_post` is the interaction of
treatment status and post-2017 indicator.

### Levels Model

The levels model replaces `log_price` with the house price level:

```text
price ~ treat_post + log_population + suburb fixed effects + year fixed effects
```

This checks whether the result depends on using logs.

### Quadratic Population Control

This model keeps `log_price` as the outcome but allows the relationship with
population to be nonlinear:

```text
log_price ~ treat_post + centered log_population + centered log_population squared
            + suburb fixed effects + year fixed effects
```

This checks whether the baseline result depends on assuming a linear population
control.

### IHS Outcome

This model uses the inverse hyperbolic sine transformation of price:

```text
price_ihs ~ treat_post + log_population + suburb fixed effects + year fixed effects
```

The IHS transformation behaves similarly to a log transformation for large
positive values, so this is an alternative outcome transformation.

### Interaction Added

This model adds an interaction between `Treat x Post` and centered log
population:

```text
log_price ~ treat_post + centered log_population
            + treat_post x centered log_population
            + suburb fixed effects + year fixed effects
```

This checks whether the treatment effect changes with suburb population size.

### 2017 Pre-Trend Test

The pre-trend test estimates treated-by-year interactions for 2015 and 2016:

```text
log_price ~ treated_x_2015 + treated_x_2016
            + log_population + suburb fixed effects + year fixed effects
```

The 2017 year is the omitted reference year. The coefficients on `treated_x_2015`
and `treated_x_2016` test whether treated suburbs were already different from
control suburbs before the 2017 milestone.

## What The Outputs Mean

### Coefficient

The coefficient is the estimated effect for the relevant model.

For the functional-form rows, the coefficient is the `Treat x Post` DiD effect.
For the pre-trend rows, the coefficient is the treated-by-year interaction for
2015 or 2016.

### HC3 Standard Error

The final table reports HC3 heteroskedasticity-robust standard errors.

HC3 adjusts the standard errors to be less sensitive to unequal error variance
across observations. It is often useful in smaller samples or when some
observations may have high leverage.

### Controls

`Controls = Yes` means the model includes population controls. In the baseline,
levels, IHS, and pre-trend models, this is `log_population`. In the quadratic
model, this is centered log population and its square. In the interaction model,
this includes centered log population and the treatment-population interaction.

### Fixed Effects

`Fixed Effects = Yes` means the model includes:

- Suburb fixed effects.
- Year fixed effects.

Suburb fixed effects control for time-invariant differences across suburbs.
Year fixed effects control for shocks common to all suburbs in a given year.

### N

`N` is the number of observations used in each regression. In the displayed
robustness table, each model uses 490 observations.

### R-squared

`R-squared` reports the share of variation in the dependent variable explained
by the model. The high values mainly reflect the inclusion of suburb and year
fixed effects.

### Joint Pre-Trend Test

The joint pre-trend test reports a p-value from a Wald test:

```text
H0: treated_x_2015 = 0 and treated_x_2016 = 0
```

A high p-value means the test does not reject the null hypothesis that the
pre-treatment coefficients are jointly zero. In plain language, this means there
is no strong statistical evidence that treated and control suburbs were already
following different trends before the 2017 milestone.

## Interpretation Summary

The functional-form checks show that the main treatment effect remains negative
across several alternative specifications. The levels model changes the unit of
interpretation because the outcome is measured in house-price dollars rather
than log points, but the direction of the effect remains negative.

The pre-trend test shows small and statistically insignificant treated-by-year
coefficients for 2015 and 2016. The joint pre-trend test does not reject the null
that these pre-treatment coefficients are jointly zero. This supports the
parallel-trends assumption needed for the DiD interpretation.

Overall, the notebook provides evidence that the main negative DiD estimate is
robust to alternative functional forms and is not contradicted by the 2017
milestone pre-trend check.
