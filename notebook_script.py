from pathlib import Path
import pandas as pd
import re
from io import StringIO

import requests

# Show all rows
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

# Find project folder
project_root = Path.cwd()
if not (project_root / "data").exists():
    project_root = project_root.parent

# ============================================================================
# SECTION 1: Clean house prices for all 57 suburbs from 2015 to 2024
# ============================================================================

# Input and output files
input_csv = project_root / "data" / "raw" / "closest_lxrp_site_house_prices_2015_2024.csv"
out_wide = project_root / "data" / "clean" / "all_suburbs_house_prices_2015_2024.csv"

# Load data
house_prices = pd.read_csv(input_csv)

# Rename suburb column neatly
house_prices = house_prices.rename(columns={"Suburb": "suburb"})

# Years to clean
years = list(range(2015, 2025))

# Clean suburb names
house_prices["suburb"] = (
    house_prices["suburb"]
    .astype(str)
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
    .str.title()
)

# Clean house price columns
for year in years:
    col = str(year)

    house_prices[col] = (
        house_prices[col]
        .astype(str)
        .str.replace(r"\\$", "", regex=True)
        .str.replace(r",", "", regex=False)
        .str.strip()
    )

    house_prices[col] = pd.to_numeric(house_prices[col], errors="coerce")

# Remove blank/messy rows
house_prices = house_prices.dropna(subset=["suburb"])
house_prices = house_prices[house_prices["suburb"] != ""]
house_prices = house_prices.dropna(subset=[str(year) for year in years], how="all")

# Remove duplicate suburbs
house_prices = house_prices.drop_duplicates(subset=["suburb"], keep="first")

# Sort alphabetically
house_prices = house_prices.sort_values("suburb").reset_index(drop=True)

# Convert price columns to integers
for year in years:
    col = str(year)
    house_prices[col] = house_prices[col].astype(int)

# Save wide version
house_prices.to_csv(out_wide, index=False)

# Print summary
print("Cleaning complete")
print(f"Saved wide file to: {out_wide}")
print(f"Number of suburbs: {house_prices['suburb'].nunique()}")
print(f"Missing values: {house_prices.isna().sum().sum()}")

# Display all suburbs and all prices
print("\nHouse Prices Data:")
print(house_prices)

# Display all suburb names only
print("\nAll Suburb Names:")
print(house_prices["suburb"].tolist())

# ============================================================================
# SECTION 2: Clean population density for all 57 suburbs from 2015 to 2024
# ============================================================================

# This file has all 57 suburbs
input_file = project_root / "data" / "clean" / "requested_suburbs_density_2015_2024_long.csv"
out_wide = project_root / "data" / "clean" / "all_57_suburbs_population_density_2015_2024.csv"

density = pd.read_csv(input_file)

# Rename columns neatly
density = density.rename(columns={
    "requested_suburb": "suburb",
    "Year": "year",
    "Density": "density",
    "Population": "population",
    "Area_km2": "area_km2",
    "SA2_components": "sa2_components"
})

# Clean suburb names
density["suburb"] = (
    density["suburb"]
    .astype(str)
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
    .str.title()
)

# Convert columns to numbers
density["year"] = pd.to_numeric(density["year"], errors="coerce")
density["density"] = pd.to_numeric(density["density"], errors="coerce")

if "population" in density.columns:
    density["population"] = pd.to_numeric(density["population"], errors="coerce")

if "area_km2" in density.columns:
    density["area_km2"] = pd.to_numeric(density["area_km2"], errors="coerce")

# Remove messy rows
density = density.dropna(subset=["suburb", "year", "density"])
density = density[density["suburb"] != ""]

# Keep 2015-2024
density["year"] = density["year"].astype(int)
density = density[(density["year"] >= 2015) & (density["year"] <= 2024)]

# Round density neatly
density["density"] = density["density"].round(2)

# Remove duplicates
density = density.drop_duplicates(subset=["suburb", "year"], keep="first")

# Sort neatly
density = density.sort_values(["suburb", "year"]).reset_index(drop=True)

# Keep useful columns
keep_cols = [
    "suburb",
    "year",
    "density",
    "population",
    "area_km2",
    "sa2_components"
]

density = density[[col for col in keep_cols if col in density.columns]]

# Create wide version
density_wide = (
    density
    .pivot(index="suburb", columns="year", values="density")
    .reset_index()
    .sort_values("suburb")
    .reset_index(drop=True)
)

density_wide.columns = ["suburb"] + [str(col) for col in density_wide.columns[1:]]

# Save wide version
density_wide.to_csv(out_wide, index=False)

print("\n" + "="*80)
print("Population density cleaning complete")
print(f"Saved wide file to: {out_wide}")
print(f"Number of suburbs: {density['suburb'].nunique()}")
print(f"Number of suburb-year rows: {len(density)}")
print(f"Missing values: {density.isna().sum().sum()}")
print(f"Duplicate suburb-year rows: {density.duplicated(['suburb', 'year']).sum()}")

print("\nPopulation Density Wide Format:")
print(density_wide)

print("\nPopulation Density Long Format:")
print(density)

# ============================================================================
# SECTION 3: Print density columns
# ============================================================================

print("\nDensity Columns:")
print(density.columns.tolist())

# ============================================================================
# SECTION 3: Daniel Bowen level-crossing classification from the November 2022 update
# ============================================================================

url = "https://danielbowen.com/2022/11/05/level-crossings-nov-2022-update/"
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

response = requests.get(url, headers=headers, timeout=30)
response.raise_for_status()
tables = pd.read_html(StringIO(response.text))


def normalize_col_name(col: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", str(col).strip().lower())


def pick_suburb_status_table(html_tables: list[pd.DataFrame]) -> tuple[pd.DataFrame, str, str]:
    candidates: list[tuple[pd.DataFrame, str, str]] = []
    for table in html_tables:
        df = table.copy()

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [" ".join([str(c) for c in col if str(c) != "nan"]).strip() for col in df.columns]

        col_map = {column: normalize_col_name(column) for column in df.columns}
        suburb_col = None
        status_col = None

        for original, normalized in col_map.items():
            if normalized in {"suburb", "suburbs"}:
                suburb_col = original
            if normalized == "status112022":
                status_col = original

        if suburb_col is not None and status_col is not None:
            candidates.append((df, suburb_col, status_col))

    if not candidates:
        raise ValueError("Could not find table with both suburb/suburbs and status 11/2022 columns.")

    return max(candidates, key=lambda item: len(item[0]))


df_raw, suburb_col, status_col = pick_suburb_status_table(tables)

df_bowen = df_raw[[suburb_col, status_col]].copy()
df_bowen.columns = ["suburb", "status"]
df_bowen["suburb"] = df_bowen["suburb"].fillna("").astype(str).str.strip().str.lower()
df_bowen["status"] = df_bowen["status"].fillna("").astype(str).str.strip().str.lower()
df_bowen = df_bowen[df_bowen["suburb"].ne("")].copy()

status_priority = {"completed": 4, "underway": 3, "planning": 2, "": 1}
df_bowen["priority"] = df_bowen["status"].map(lambda status: status_priority.get(status, 1))

df_bowen_suburb = (
    df_bowen.sort_values("priority", ascending=False)
    .drop_duplicates(subset=["suburb"], keep="first")
    .loc[:, ["suburb", "status"]]
    .sort_values("suburb")
    .reset_index(drop=True)
)

treated_statuses = {"completed", "planning", "underway"}
df_bowen_suburb["treated"] = df_bowen_suburb["status"].apply(lambda status: 1.0 if status in treated_statuses else 0.0)

treated_bowen = df_bowen_suburb[df_bowen_suburb["treated"] == 1.0].reset_index(drop=True)
untreated_bowen = df_bowen_suburb[df_bowen_suburb["treated"] == 0.0].reset_index(drop=True)

print("\nDaniel Bowen — classification using Suburb/Suburbs + Status 11/2022 only")
print(f"Total unique suburbs from the page: {len(df_bowen_suburb)}")
print(f"Treated (completed/planning/underway): {len(treated_bowen)}")
print(f"Untreated (other/blank): {len(untreated_bowen)}")
print("\nTREATED suburbs (treated = 1.0):")
print(treated_bowen)
print("\nUNTREATED suburbs (treated = 0.0):")
print(untreated_bowen)

