from __future__ import annotations

import argparse
import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def find_project_root(start: Path | None = None) -> Path:
    here = (start or Path.cwd()).resolve()
    candidates = [here, *here.parents]
    for path in candidates:
        if (path / "data" / "clean").exists():
            return path
    return here


def melt_wide(df: pd.DataFrame, year_str: list[str], value_name: str) -> pd.DataFrame:
    out = df.melt(id_vars=["Suburb"], value_vars=year_str, var_name="Year", value_name=value_name)
    out["Year"] = pd.to_numeric(out["Year"], errors="coerce").astype(int)
    out[value_name] = pd.to_numeric(out[value_name], errors="coerce")
    return out


def build_lxrp_table() -> pd.DataFrame:
    suburbs = [
        ("Chelsea", 4), ("Laverton", 3), ("Ringwood", 2), ("Mentone", 2), ("Preston", 1),
        ("Blackburn", 2), ("Beaconsfield", 2), ("Essendon", 1), ("Glen Iris", 1),
        ("Cranbourne", 3), ("Campbellfield", 3), ("Pakenham", 3), ("Lilydale", 2),
        ("Bentleigh", 1), ("Clayton", 2), ("Noble Park", 2), ("Cheltenham", 2),
        ("Werribee", 3), ("Berwick", 3), ("Croydon", 0), ("Edithvale", 2),
        ("Williamstown", 1), ("Ardeer", 1), ("St Albans", 1), ("Sunbury", 2),
        ("Glenroy", 0), ("Alphington", 1), ("Carnegie", 1), ("Hallam", 3),
        ("Mitcham", 2), ("Reservoir", 0), ("Coburg", 0), ("Brunswick", 0), ("Bundoora", 4),
        ("Doncaster", 10), ("Doncaster East", 12), ("Donvale", 9), ("Templestowe", 8),
        ("Templestowe Lower", 6), ("Warrandyte", 12), ("Wonga Park", 15), ("Park Orchards", 9),
        ("Bulleen", 10), ("Rowville", 10), ("Lysterfield", 11), ("Scoresby", 9),
        ("Knoxfield", 9), ("Wantirna", 6), ("Wantirna South", 7), ("The Basin", 7),
        ("Endeavour Hills", 6), ("Doveton", 4), ("Greenvale", 7), ("Gladstone Park", 6),
        ("Westmeadows", 3), ("Tullamarine", 6), ("Keilor East", 4),
    ]
    return pd.DataFrame(suburbs, columns=["Suburb", "nearest_lxrp_site"]).drop_duplicates("Suburb")


def build_density_tables(root: Path, years: list[int]) -> pd.DataFrame:
    base_suburbs = [
        "Chelsea", "Laverton", "Ringwood", "Mentone", "Preston", "Blackburn",
        "Beaconsfield", "Essendon", "Glen Iris", "Cranbourne", "Campbellfield",
        "Pakenham", "Lilydale", "Bentleigh", "Clayton", "Noble Park",
        "Cheltenham", "Werribee", "Berwick", "Croydon", "Edithvale",
        "Williamstown", "Ardeer", "St Albans", "Sunbury", "Glenroy",
        "Alphington", "Carnegie", "Hallam", "Mitcham", "Reservoir",
        "Coburg", "Brunswick", "Bundoora",
    ]
    new_suburbs = [
        "Doncaster", "Doncaster East", "Donvale", "Templestowe", "Templestowe Lower",
        "Warrandyte", "Wonga Park", "Park Orchards", "Bulleen", "Rowville",
        "Lysterfield", "Scoresby", "Knoxfield", "Wantirna", "Wantirna South",
        "The Basin", "Endeavour Hills", "Doveton", "Greenvale", "Gladstone Park",
        "Westmeadows", "Tullamarine", "Keilor East",
    ]

    def unique_in_order(items: list[str]) -> list[str]:
        seen, out = set(), []
        for item in items:
            item = str(item).strip()
            if item and item not in seen:
                seen.add(item)
                out.append(item)
        return out

    suburbs = unique_in_order(base_suburbs + new_suburbs)

    sa2_map = {
        "Chelsea": ["Chelsea - Bonbeach"],
        "Cheltenham": ["Highett (East) - Cheltenham", "Highett (West) - Cheltenham"],
        "Doncaster East": ["Doncaster East - North", "Doncaster East - South"],
        "Donvale": ["Donvale - Park Orchards"],
        "Park Orchards": ["Donvale - Park Orchards"],
        "Warrandyte": ["Warrandyte - Wonga Park"],
        "Wonga Park": ["Warrandyte - Wonga Park"],
        "Rowville": ["Rowville - Central", "Rowville - North", "Rowville - South"],
        "Scoresby": ["Knoxfield - Scoresby"],
        "Knoxfield": ["Knoxfield - Scoresby"],
        "Endeavour Hills": ["Endeavour Hills - North", "Endeavour Hills - South"],
        "Greenvale": ["Greenvale - Bulla"],
        "Gladstone Park": ["Gladstone Park - Westmeadows"],
        "Westmeadows": ["Gladstone Park - Westmeadows"],
    }

    pop_path = root / "data" / "raw" / "abs_population.xlsx"
    sa2_area_path = root / "data" / "raw" / "SA2_2021_AUST.xlsx"
    out_long = root / "data" / "clean" / "requested_suburbs_density_2015_2024_long.csv"
    out_wide = root / "data" / "clean" / "requested_suburbs_density_2015_2024.csv"

    hdr = pd.read_excel(pop_path, sheet_name="Table 1", header=None, nrows=6)
    colnames = hdr.iloc[5, :10].tolist() + hdr.iloc[4, 10:].tolist()

    pop = pd.read_excel(pop_path, sheet_name="Table 1", header=None, skiprows=6)
    pop.columns = colnames
    pop["S/T name"] = pop["S/T name"].astype(str).str.strip()
    pop = pop[pop["S/T name"].eq("Victoria")].copy()
    pop["SA2 code"] = pd.to_numeric(pop["SA2 code"], errors="coerce").astype("Int64")
    pop["SA2 name"] = pop["SA2 name"].astype(str).str.strip()

    for year in years:
        pop[year] = pd.to_numeric(pop[year], errors="coerce")

    sa2 = pd.read_excel(
        sa2_area_path,
        usecols=["SA2_CODE_2021", "SA2_NAME_2021", "AREA_ALBERS_SQKM", "STATE_NAME_2021"],
    )
    sa2["STATE_NAME_2021"] = sa2["STATE_NAME_2021"].astype(str).str.strip()
    sa2 = sa2[sa2["STATE_NAME_2021"].eq("Victoria")].copy()
    sa2["SA2_CODE_2021"] = pd.to_numeric(sa2["SA2_CODE_2021"], errors="coerce").astype("Int64")
    sa2["SA2_NAME_2021"] = sa2["SA2_NAME_2021"].astype(str).str.strip()
    sa2 = sa2.rename(columns={"AREA_ALBERS_SQKM": "sa2_area_km2"})

    pop = pop.merge(
        sa2[["SA2_CODE_2021", "sa2_area_km2"]],
        left_on="SA2 code",
        right_on="SA2_CODE_2021",
        how="left",
    )

    sa2_names_all = set(pop["SA2 name"].dropna().unique())

    def resolve_sa2_names(suburb: str) -> list[str]:
        if suburb in sa2_map:
            return sa2_map[suburb]
        if suburb in sa2_names_all:
            return [suburb]

        starts_with_dash = sorted([n for n in sa2_names_all if n.lower().startswith(suburb.lower() + " -")])
        if starts_with_dash:
            return starts_with_dash

        pattern = re.compile(rf"\b{re.escape(suburb)}\b", flags=re.IGNORECASE)
        matches = sorted([n for n in sa2_names_all if pattern.search(n)])
        if not matches:
            raise ValueError(f"No SA2 match found for suburb: {suburb}")
        return matches

    rows = []
    for suburb in suburbs:
        sa2_names = resolve_sa2_names(suburb)
        sub = pop[pop["SA2 name"].isin(sa2_names)].copy()
        if sub.empty:
            continue

        area_total = (
            sub[["SA2 code", "sa2_area_km2"]]
            .drop_duplicates()["sa2_area_km2"]
            .sum(min_count=1)
        )
        if pd.isna(area_total) or area_total == 0:
            raise ValueError(f"Missing or zero area for suburb: {suburb} | SA2: {sa2_names}")

        for year in years:
            pop_total = sub[year].sum(min_count=1)
            density = pop_total / area_total if pd.notna(pop_total) else pd.NA
            rows.append(
                {
                    "Suburb": suburb,
                    "Year": year,
                    "Population": pop_total,
                    "Area_km2": area_total,
                    "Density": density,
                    "SA2_components": " | ".join(sa2_names),
                }
            )

    long_df = pd.DataFrame(rows)
    long_df["Suburb"] = pd.Categorical(long_df["Suburb"], categories=suburbs, ordered=True)
    long_df = long_df.sort_values(["Suburb", "Year"]).reset_index(drop=True)

    wide = (
        long_df.pivot(index="Suburb", columns="Year", values="Density")
        .reindex(suburbs)
        .reset_index()
    )
    wide.columns = ["Suburb"] + [str(y) for y in years]
    wide.insert(0, "No.", range(1, len(wide) + 1))

    long_df.to_csv(out_long, index=False)
    wide.to_csv(out_wide, index=False)
    return wide


def prepare_panel(root: Path, years: list[int]) -> tuple[pd.DataFrame, pd.DataFrame]:
    clean = root / "data" / "clean"
    year_str = [str(y) for y in years]

    density_file = clean / "requested_suburbs_density_2015_2024.csv"
    if density_file.exists():
        density_wide = pd.read_csv(density_file).drop(columns=["No."], errors="ignore")
    else:
        density_wide = build_density_tables(root, years).drop(columns=["No."], errors="ignore")

    price_wide = pd.read_csv(clean / "closest_lxrp_site_house_prices_2015_2024.csv")
    income = pd.read_csv(clean / "annual_household_income_table.csv")
    lxrp = build_lxrp_table()

    adjacent_suburbs = set(
        pd.read_csv(clean / "adjacent_suburbs_house_prices_2015_2024.csv")["Suburb"].astype(str).str.strip()
    )
    faraway_suburbs = set(
        pd.read_csv(clean / "faraway_suburbs_house_prices_2015_2024.csv")["Suburb"].astype(str).str.strip()
    )

    density_long = melt_wide(density_wide, year_str, "Density")
    price_long = melt_wide(price_wide, year_str, "HousePrice")

    panel = (
        price_long
        .merge(density_long, on=["Suburb", "Year"], how="inner")
        .merge(lxrp, on="Suburb", how="left")
        .merge(
            income.rename(columns={"Annual total household income ($/year)": "AnnualIncome"}),
            on="Suburb",
            how="left",
        )
    )

    panel["Group"] = "Unclassified"
    panel.loc[panel["Suburb"].isin(adjacent_suburbs), "Group"] = "Adjacent"
    panel.loc[panel["Suburb"].isin(faraway_suburbs), "Group"] = "Faraway"
    panel = panel[panel["Group"].isin(["Adjacent", "Faraway"])].copy()
    panel["log_HousePrice"] = np.log(panel["HousePrice"])
    panel["log_Density"] = np.log(panel["Density"].clip(lower=1e-9))

    grouped_yearly = panel.groupby(["Year", "Group"], as_index=False).agg(
        HousePriceMedian=("HousePrice", "median"),
        DensityMedian=("Density", "median"),
    )
    return panel, grouped_yearly


def save_fig(path: Path, show: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path, dpi=200, bbox_inches="tight")
    if show:
        plt.show()
    plt.close()


def run_eda(root: Path, out_dir: Path, show: bool = False) -> None:
    years = list(range(2015, 2025))
    clean = root / "data" / "clean"

    panel, grouped_yearly = prepare_panel(root, years)

    # Graph 1: ranked suburb median price
    suburb_median = panel.groupby("Suburb", as_index=False)["HousePrice"].median().sort_values("HousePrice", ascending=False)
    plt.figure(figsize=(8, 12))
    plt.hlines(y=suburb_median["Suburb"], xmin=0, xmax=suburb_median["HousePrice"], color="#4C78A8", alpha=0.5)
    plt.plot(suburb_median["HousePrice"], suburb_median["Suburb"], "o", color="#1f4e79")
    plt.title("Median House Price by Suburb (Ranked)")
    plt.xlabel("Median House Price")
    plt.ylabel("Suburb")
    save_fig(out_dir / "01_ranked_median_house_price.png", show)

    # Graph 2: adjacent price distribution
    adjacent_df = pd.read_csv(clean / "adjacent_suburbs_house_prices_2015_2024.csv")
    year_cols = [str(y) for y in years]
    adjacent_values = adjacent_df[year_cols].apply(pd.to_numeric, errors="coerce").to_numpy().flatten()
    adjacent_values = pd.Series(adjacent_values).dropna().values
    plt.figure(figsize=(8, 7))
    plt.boxplot([adjacent_values], tick_labels=["Adjacent suburbs"], showfliers=True, patch_artist=True)
    plt.ylabel("Median House Price (AUD)")
    plt.title("Grouped box-and-whisker plot: adjacent suburbs (2015-2024)")
    save_fig(out_dir / "02_adjacent_price_boxplot.png", show)

    # Graph 3: faraway price distribution
    faraway_df = pd.read_csv(clean / "faraway_suburbs_house_prices_2015_2024.csv")
    faraway_values = faraway_df[year_cols].apply(pd.to_numeric, errors="coerce").to_numpy().flatten()
    faraway_values = pd.Series(faraway_values).dropna().values
    plt.figure(figsize=(8, 7))
    plt.boxplot([faraway_values], tick_labels=["Faraway suburbs"], showfliers=True, patch_artist=True)
    plt.ylabel("Median House Price (AUD)")
    plt.title("Grouped box-and-whisker plot: faraway suburbs (2015-2024)")
    save_fig(out_dir / "03_faraway_price_boxplot.png", show)

    # Graph 4: overall density distribution
    density_wide = pd.read_csv(clean / "requested_suburbs_density_2015_2024.csv")
    density_cols = [c for c in density_wide.columns if c not in ["No.", "Suburb"]]
    density_values = density_wide[density_cols].apply(pd.to_numeric, errors="coerce").to_numpy().ravel()
    density_values = density_values[~pd.isna(density_values)]
    plt.figure(figsize=(7, 7))
    plt.boxplot([density_values], tick_labels=["All suburbs"], vert=True, showfliers=False, patch_artist=True)
    plt.title("Population Density Across All Suburbs (2015-2024)")
    plt.ylabel("Population Density")
    save_fig(out_dir / "04_density_boxplot.png", show)

    # Graph 5: grouped house price trend
    plt.figure(figsize=(8, 4))
    for grp in ["Adjacent", "Faraway"]:
        tmp = grouped_yearly[grouped_yearly["Group"] == grp]
        plt.plot(tmp["Year"], tmp["HousePriceMedian"], marker="o", label=f"{grp} suburbs")
    plt.title("Overall House Price Trend by Suburb Group")
    plt.xlabel("Year")
    plt.ylabel("Median House Price")
    plt.legend()
    save_fig(out_dir / "05_grouped_house_price_trend.png", show)

    # Graph 6: grouped density trend
    plt.figure(figsize=(8, 4))
    for grp in ["Adjacent", "Faraway"]:
        tmp = grouped_yearly[grouped_yearly["Group"] == grp]
        plt.plot(tmp["Year"], tmp["DensityMedian"], marker="o", label=f"{grp} suburbs")
    plt.title("Overall Density Trend by Suburb Group")
    plt.xlabel("Year")
    plt.ylabel("Median Density")
    plt.legend()
    save_fig(out_dir / "06_grouped_density_trend.png", show)

    # Graph 7: scatter house price vs density
    plt.figure(figsize=(7, 5))
    sns.scatterplot(data=panel, x="Density", y="HousePrice", hue="Year", palette="viridis", s=40, alpha=0.75)
    sns.regplot(data=panel, x="Density", y="HousePrice", scatter=False, color="black")
    plt.title("House Price vs Population Density")
    save_fig(out_dir / "07_scatter_price_vs_density.png", show)

    # Graph 8: correlation heatmap
    corr_cols = ["HousePrice", "Density", "nearest_lxrp_site", "AnnualIncome", "Year", "log_HousePrice", "log_Density"]
    corr = panel[corr_cols].corr(numeric_only=True)
    plt.figure(figsize=(7.5, 6))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", center=0)
    plt.title("Correlation Heatmap")
    save_fig(out_dir / "08_correlation_heatmap.png", show)

    # Graph 9: between vs within
    between = panel.groupby("Suburb", as_index=False)[["HousePrice", "Density"]].mean()
    within = panel.copy()
    within["HousePrice_w"] = within["HousePrice"] - within.groupby("Suburb")["HousePrice"].transform("mean")
    within["Density_w"] = within["Density"] - within.groupby("Suburb")["Density"].transform("mean")

    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    sns.regplot(data=between, x="Density", y="HousePrice", ax=axs[0], scatter_kws={"s": 35})
    axs[0].set_title("Between-Suburb Relationship")
    sns.regplot(data=within, x="Density_w", y="HousePrice_w", ax=axs[1], scatter_kws={"s": 18, "alpha": 0.5})
    axs[1].set_title("Within-Suburb Relationship")
    save_fig(out_dir / "09_between_vs_within.png", show)

    # Graph 10: OLS diagnostics
    ols = panel[["HousePrice", "Density", "nearest_lxrp_site", "Year"]].dropna().copy()
    X = np.column_stack([
        np.ones(len(ols)),
        ols["Density"].to_numpy(),
        ols["nearest_lxrp_site"].to_numpy(),
        ols["Year"].to_numpy(),
    ])
    y = ols["HousePrice"].to_numpy()
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    fitted = X @ beta
    resid = y - fitted

    fig, axs = plt.subplots(1, 2, figsize=(11, 4))
    axs[0].scatter(fitted, resid, alpha=0.55, s=20)
    axs[0].axhline(0, color="black", lw=1)
    axs[0].set_title("Residuals vs Fitted")
    axs[0].set_xlabel("Fitted")
    axs[0].set_ylabel("Residual")

    n = len(resid)
    obs = np.sort((resid - resid.mean()) / (resid.std(ddof=1) + 1e-12))
    probs = (np.arange(1, n + 1) - 0.5) / n
    x = 2 * probs - 1
    a = 0.147
    ln = np.log(1 - x * x + 1e-12)
    theor = np.sqrt(2) * np.sign(x) * np.sqrt(np.sqrt((2 / (np.pi * a) + ln / 2) ** 2 - ln / a) - (2 / (np.pi * a) + ln / 2))

    mn, mx = min(theor.min(), obs.min()), max(theor.max(), obs.max())
    axs[1].scatter(theor, obs, alpha=0.55, s=20)
    axs[1].plot([mn, mx], [mn, mx], color="black", lw=1)
    axs[1].set_title("Q-Q Plot (Standardized Residuals)")
    axs[1].set_xlabel("Theoretical Quantiles")
    axs[1].set_ylabel("Observed Quantiles")
    save_fig(out_dir / "10_ols_diagnostics.png", show)

    print(f"Saved EDA figures to: {out_dir}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run EDA workflow from EDA.ipynb as a standalone script.")
    parser.add_argument("--project-root", type=str, default=None, help="Optional explicit project root path.")
    parser.add_argument("--output-dir", type=str, default="outputs/eda_figures", help="Directory for exported figure files.")
    parser.add_argument("--show", action="store_true", help="Show figures interactively in addition to saving.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(args.project_root).resolve() if args.project_root else find_project_root()
    out_dir = (root / args.output_dir).resolve()
    run_eda(root=root, out_dir=out_dir, show=args.show)


if __name__ == "__main__":
    main()
