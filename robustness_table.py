from pathlib import Path
import sys

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = PROJECT_ROOT / "results"

if str(PROJECT_ROOT / "code") not in sys.path:
    sys.path.append(str(PROJECT_ROOT / "code"))

from robustness_alternative_inference import build_panel, stars


def prepare_data():
    df = build_panel().copy()
    df["price_ihs"] = np.arcsinh(df["price"])
    df["log_population_centered"] = (
        df["log_population"] - df["log_population"].mean()
    )
    df["log_population_centered_sq"] = df["log_population_centered"] ** 2
    return df


def fit_functional_form_models(df):
    formulas = {
        "Main specification": (
            "log_price ~ treat_post + log_population + C(suburb) + C(year)"
        ),
        "Levels model": (
            "price ~ treat_post + log_population + C(suburb) + C(year)"
        ),
        "Quadratic control": (
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
        df[f"treated_x_{year}"] = (
            df["treated"] * (df["year"] == year).astype(int)
        )

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
    table = pd.DataFrame(
        {
            "Statistic": [
                "Treat x Post coefficient",
                "HC3 standard error",
                "t-statistic",
                "Pretrend: Treat x 2015",
                "Pretrend: Treat x 2015 HC3 SE",
                "Pretrend: Treat x 2016",
                "Pretrend: Treat x 2016 HC3 SE",
                "Joint pretrend p-value",
                "N",
                "R-squared",
            ]
        }
    )

    for label, result in results.items():
        table[label] = [
            coefficient(result, "treat_post"),
            standard_error(result, "treat_post"),
            f"{result.tvalues['treat_post']:.3f}",
            "",
            "",
            "",
            "",
            "",
            f"{int(result.nobs):,}",
            f"{result.rsquared:.3f}",
        ]

    table["Pretrend test"] = [
        "",
        "",
        "",
        coefficient(pretrend_result, "treated_x_2015"),
        standard_error(pretrend_result, "treated_x_2015"),
        coefficient(pretrend_result, "treated_x_2016"),
        standard_error(pretrend_result, "treated_x_2016"),
        f"{float(joint_test.pvalue):.3f}",
        f"{int(pretrend_result.nobs):,}",
        f"{pretrend_result.rsquared:.3f}",
    ]

    return table


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
        "Notes: Each column reports a separate specification or robustness check. "
        "Column 1 is the main log-price DiD specification. Column 2 estimates the "
        "model using house price in levels instead of log house price. Column 3 "
        "keeps log house price as the outcome but adds a quadratic in centered log "
        "population. Column 4 uses the inverse hyperbolic sine transformation of "
        "house price as the outcome. Column 5 adds an interaction between Treat x "
        "Post and centered log population, so the Treat x Post coefficient is "
        "evaluated at mean log population. Column 6 reports the 2017 milestone "
        "pretrend test using treated-by-year interactions for 2015 and 2016; the "
        "joint pretrend p-value tests whether both pre-treatment interactions are "
        "equal to zero. All specifications include population controls, suburb "
        "fixed effects, and year fixed effects. Standard errors are HC3 "
        "heteroskedasticity-robust standard errors and are reported in parentheses. "
        "N is reported in every column. *, **, and *** denote significance at the "
        "10%, 5%, and 1% levels."
    )


def build_interpretation(joint_test):
    return (
        "The robustness checks support the main DiD result. The Treat x Post "
        "coefficient remains negative across the alternative functional-form "
        "models, suggesting that the result is not driven by one particular "
        "outcome transformation or population-control specification. The levels "
        "model is measured in dollar units, so its magnitude is not directly "
        "comparable with the log and IHS specifications. The pretrend coefficients "
        "for 2015 and 2016 are small, and the joint pretrend p-value is "
        f"{float(joint_test.pvalue):.3f}, so the test does not reject the null "
        "that the pre-treatment interactions are jointly zero. This provides no "
        "strong evidence against parallel trends before the 2017 milestone."
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
