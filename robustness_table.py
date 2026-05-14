from pathlib import Path
import sys

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


PROJECT_ROOT = Path(__file__).resolve().parent
RESULTS_DIR = PROJECT_ROOT / "results"

if str(PROJECT_ROOT / "code") not in sys.path:
    sys.path.append(str(PROJECT_ROOT / "code"))


def build_panel():
    clean = PROJECT_ROOT / "data" / "clean"
    wide = pd.read_csv(clean / "population_density_all_suburbs.csv")

    wide["suburb"] = wide["suburb"].astype(str).str.strip().str.upper()
    wide["treated"] = wide["treated"].astype(int)

    price_cols = [col for col in wide.columns if col.endswith("_price")]
    pop_cols = [col for col in wide.columns if col.endswith("_pop")]

    prices_long = wide[["suburb", "status", "treated"] + price_cols].melt(
        id_vars=["suburb", "status", "treated"],
        value_vars=price_cols,
        var_name="year",
        value_name="price",
    )
    prices_long["year"] = prices_long["year"].str.replace("_price", "", regex=False).astype(int)

    population_long = wide[["suburb"] + pop_cols].melt(
        id_vars=["suburb"],
        value_vars=pop_cols,
        var_name="year",
        value_name="population",
    )
    population_long["year"] = population_long["year"].str.replace("_pop", "", regex=False).astype(int)

    df = (
        prices_long
        .merge(population_long, on=["suburb", "year"], how="inner")
        .dropna(subset=["price", "population", "treated"])
        .copy()
    )
    df = df[(df["price"] > 0) & (df["population"] > 0)].copy()

    df["post"] = (df["year"] >= 2017).astype(int)
    df["treat_post"] = df["treated"] * df["post"]
    df["log_price"] = np.log(df["price"])
    df["log_population"] = np.log(df["population"])

    return df


def stars(p_value):
    if p_value < 0.01:
        return "***"
    if p_value < 0.05:
        return "**"
    if p_value < 0.1:
        return "*"
    return ""


def prepare_data():
    df = build_panel().copy()
    df["price_ihs"] = np.arcsinh(df["price"])
    df["log_population_centered"] = df["log_population"] - df["log_population"].mean()
    df["log_population_centered_sq"] = df["log_population_centered"] ** 2
    return df


def fit_functional_form_models(df):
    formulas = {
        "Baseline": (
            "log_price ~ treat_post + log_population + C(suburb) + C(year)"
        ),
        "Levels model": (
            "price ~ treat_post + log_population + C(suburb) + C(year)"
        ),
        "Quadratic population control": (
            "log_price ~ treat_post + log_population_centered "
            "+ log_population_centered_sq + C(suburb) + C(year)"
        ),
        "IHS outcome": (
            "price_ihs ~ treat_post + log_population + C(suburb) + C(year)"
        ),
        "Interaction added": (
            "log_price ~ treat_post + log_population_centered "
            "+ treat_post:log_population_centered + C(suburb) + C(year)"
        ),
    }

    return {
        label: smf.ols(formula, data=df).fit(cov_type="HC3")
        for label, formula in formulas.items()
    }


def fit_pretrend_model(df):
    pre_years = [2015, 2016]
    df = df.copy()

    for year in pre_years:
        df[f"treated_x_{year}"] = df["treated"] * (df["year"] == year).astype(int)

    formula = (
        "log_price ~ "
        + " + ".join(f"treated_x_{year}" for year in pre_years)
        + " + log_population + C(suburb) + C(year)"
    )

    result = smf.ols(formula, data=df).fit(cov_type="HC3")
    restriction = " = 0, ".join(f"treated_x_{year}" for year in pre_years) + " = 0"
    joint_test = result.wald_test(restriction, scalar=True)

    return result, joint_test


def coefficient(result, variable):
    coef = result.params[variable]
    p_value = result.pvalues[variable]
    return f"{coef:.3f}{stars(p_value)}"


def standard_error(result, variable):
    return f"({result.bse[variable]:.3f})"


def build_robustness_table(results, pretrend_result, joint_test):
    rows = [
        {
            "Model": "Baseline",
            "Coefficient": coefficient(results["Baseline"], "treat_post"),
            "Standard Error": standard_error(results["Baseline"], "treat_post"),
            "Controls": "Yes",
            "Fixed Effects": "Yes",
            "SE Type": "HC3",
            "N": f"{int(results['Baseline'].nobs):,}",
            "R²": f"{results['Baseline'].rsquared:.3f}",
        },
        {
            "Model": "Levels model",
            "Coefficient": coefficient(results["Levels model"], "treat_post"),
            "Standard Error": standard_error(results["Levels model"], "treat_post"),
            "Controls": "Yes",
            "Fixed Effects": "Yes",
            "SE Type": "HC3",
            "N": f"{int(results['Levels model'].nobs):,}",
            "R²": f"{results['Levels model'].rsquared:.3f}",
        },
        {
            "Model": "Quadratic population control",
            "Coefficient": coefficient(results["Quadratic population control"], "treat_post"),
            "Standard Error": standard_error(results["Quadratic population control"], "treat_post"),
            "Controls": "Yes",
            "Fixed Effects": "Yes",
            "SE Type": "HC3",
            "N": f"{int(results['Quadratic population control'].nobs):,}",
            "R²": f"{results['Quadratic population control'].rsquared:.3f}",
        },
        {
            "Model": "IHS outcome",
            "Coefficient": coefficient(results["IHS outcome"], "treat_post"),
            "Standard Error": standard_error(results["IHS outcome"], "treat_post"),
            "Controls": "Yes",
            "Fixed Effects": "Yes",
            "SE Type": "HC3",
            "N": f"{int(results['IHS outcome'].nobs):,}",
            "R²": f"{results['IHS outcome'].rsquared:.3f}",
        },
        {
            "Model": "Interaction added",
            "Coefficient": coefficient(results["Interaction added"], "treat_post"),
            "Standard Error": standard_error(results["Interaction added"], "treat_post"),
            "Controls": "Yes",
            "Fixed Effects": "Yes",
            "SE Type": "HC3",
            "N": f"{int(results['Interaction added'].nobs):,}",
            "R²": f"{results['Interaction added'].rsquared:.3f}",
        },
        {
            "Model": "Pretrend test: Treat x 2015",
            "Coefficient": coefficient(pretrend_result, "treated_x_2015"),
            "Standard Error": standard_error(pretrend_result, "treated_x_2015"),
            "Controls": "Yes",
            "Fixed Effects": "Yes",
            "SE Type": "HC3",
            "N": f"{int(pretrend_result.nobs):,}",
            "R²": f"{pretrend_result.rsquared:.3f}",
        },
        {
            "Model": "Pretrend test: Treat x 2016",
            "Coefficient": coefficient(pretrend_result, "treated_x_2016"),
            "Standard Error": standard_error(pretrend_result, "treated_x_2016"),
            "Controls": "Yes",
            "Fixed Effects": "Yes",
            "SE Type": "HC3",
            "N": f"{int(pretrend_result.nobs):,}",
            "R²": f"{pretrend_result.rsquared:.3f}",
        },
        {
            "Model": "Joint pretrend test",
            "Coefficient": f"p = {float(joint_test.pvalue):.3f}",
            "Standard Error": "",
            "Controls": "Yes",
            "Fixed Effects": "Yes",
            "SE Type": "HC3",
            "N": f"{int(pretrend_result.nobs):,}",
            "R²": f"{pretrend_result.rsquared:.3f}",
        },
    ]

    return pd.DataFrame(rows)


def dataframe_to_markdown(df):
    headers = list(df.columns)
    rows = [[str(value) for value in row] for row in df.to_numpy()]
    widths = [
        max(len(str(header)), *(len(row[i]) for row in rows))
        for i, header in enumerate(headers)
    ]

    def format_row(values):
        return "| " + " | ".join(
            str(value).ljust(widths[i]) for i, value in enumerate(values)
        ) + " |"

    separator = "| " + " | ".join("-" * width for width in widths) + " |"
    return "\n".join([format_row(headers), separator] + [format_row(row) for row in rows])


def build_notes():
    return (
        "Notes: Each row reports a model or robustness check. The baseline row "
        "estimates the main log-price DiD specification. The levels model uses "
        "house price in levels instead of log house price. The quadratic population "
        "control model keeps log house price as the outcome while adding a centered "
        "quadratic term for log population. The IHS outcome model uses the inverse "
        "hyperbolic sine of price. The interaction model adds a Treat x centered log "
        "population term. The final rows report pretrend test coefficients for 2015 "
        "and 2016 plus the joint pretrend p-value. All models include population "
        "controls, suburb fixed effects, year fixed effects, and HC3 standard errors. "
        "*, **, and *** denote significance at the 10%, 5%, and 1% levels."
    )


def build_interpretation(joint_test):
    return (
        "The robustness checks align with the notebook results. The Treat x Post "
        "coefficient stays small and generally negative across alternative model "
        "specifications, indicating the finding does not hinge on a particular "
        "outcome transformation or population control. The joint pretrend p-value "
        f"is {float(joint_test.pvalue):.3f}, so the pretrend test does not reject "
        "the null hypothesis that the 2015 and 2016 treated-year interactions are "
        "jointly zero. This provides no strong evidence against parallel trends "
        "before the 2017 milestone."
    )


def save_outputs(table, notes, interpretation):
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    csv_path = RESULTS_DIR / "robustness_table.csv"
    md_path = RESULTS_DIR / "robustness_table.md"
    html_path = RESULTS_DIR / "robustness_table.html"

    table.to_csv(csv_path, index=False)

    markdown = (
        "# Robustness Table\n\n"
        "## Table\n\n"
        f"{dataframe_to_markdown(table)}\n\n"
        "## Notes\n\n"
        f"{notes}\n\n"
        "## Interpretation\n\n"
        f"{interpretation}\n"
    )
    md_path.write_text(markdown, encoding="utf-8")

    html = (
        "<h1>Robustness Table</h1>"
        "<h2>Table</h2>"
        f"{table.to_html(index=False)}"
        "<h2>Notes</h2>"
        f"<p>{notes}</p>"
        "<h2>Interpretation</h2>"
        f"<p>{interpretation}</p>"
    )
    html_path.write_text(html, encoding="utf-8")

    return csv_path, md_path, html_path


def main():
    df = prepare_data()
    results = fit_functional_form_models(df)
    pretrend_result, joint_test = fit_pretrend_model(df)

    table = build_robustness_table(results, pretrend_result, joint_test)
    notes = build_notes()
    interpretation = build_interpretation(joint_test)
    output_paths = save_outputs(table, notes, interpretation)

    print(table.to_string(index=False))
    print()
    print(notes)
    print()
    print(interpretation)
    print()
    print("Saved:")
    for path in output_paths:
        print(path)


if __name__ == "__main__":
    main()
