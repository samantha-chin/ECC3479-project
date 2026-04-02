
# Cell 3
import pandas as pd
from pathlib import Path

file_path = r"C:\Users\samantha\Downloads\Bundoora avg inc.xlsx"
df = pd.read_excel(file_path, sheet_name="G02")  # read the Excel file & specify the sheet needed

print(df.head())  # print the first few rows of the dataframe to check if it was read correctly


# Cell 4
# clean Bundoora G02 data & saving it to data/clean/
project_root = Path.cwd().parent
raw_csv = project_root / "data" / "raw" / "all_rows_G02.csv"
clean_csv = project_root / "data" / "clean" / "all_rows_G02_clean.csv"

g02 = pd.read_csv(raw_csv, header=None, dtype=str, keep_default_na=True)

left = g02[[0, 1]].rename(columns={0: "metric", 1: "value"})
right = g02[[3, 4]].rename(columns={3: "metric", 4: "value"})
combined = pd.concat([left, right], ignore_index=True)

combined["metric"] = combined["metric"].astype(str).str.strip()
combined["value"] = combined["value"].astype(str).str.strip()
combined = combined.replace({"": pd.NA, "nan": pd.NA, "NaN": pd.NA, "NAN": pd.NA})
combined = combined.dropna(subset=["metric", "value"])
combined = combined[~combined["metric"].str.contains("AUSTRALIAN BUREAU|G02 SELECTED|Unnamed", na=False)]
combined["value"] = pd.to_numeric(combined["value"], errors="coerce")
cleaned = combined.dropna(subset=["value"]).reset_index(drop=True)

clean_csv.parent.mkdir(parents=True, exist_ok=True)
cleaned.to_csv(clean_csv, index=False)
cleaned.to_excel(clean_xlsx, index=False)

print(f"Saved {len(cleaned)} rows to {clean_csv}")
display(cleaned)


# Cell 6
# generate and clean Sunshine G02 output (removing NaN/blank values)

import pandas as pd
from pathlib import Path

file_path = r"C:\Users\samantha\Downloads\GCP_SAL22395.xlsx"
raw_g02 = pd.read_excel(file_path, sheet_name="G02", header=None, dtype=str)

left = raw_g02[[0, 1]].rename(columns={0: "metric", 1: "value"})
right = raw_g02[[3, 4]].rename(columns={3: "metric", 4: "value"})
combined = pd.concat([left, right], ignore_index=True)

combined["metric"] = combined["metric"].str.strip()
combined["value"] = combined["value"].str.strip()
combined = combined.replace({"": pd.NA, "nan": pd.NA, "NaN": pd.NA, "NAN": pd.NA})
combined = combined.dropna(subset=["metric", "value"])

combined = combined[
    ~combined["metric"].str.contains(
        r"AUSTRALIAN BUREAU|G02 SELECTED|List of tables|sq Kms|Unnamed",
        case=False,
        na=False,
    )
]

combined["value"] = pd.to_numeric(combined["value"], errors="coerce")
sunshine_clean = combined.dropna(subset=["value"]).reset_index(drop=True)

project_root = Path.cwd().parent
clean_csv = project_root / "data" / "clean" / "sunshine_G02_clean.csv"
clean_csv.parent.mkdir(parents=True, exist_ok=True)

sunshine_clean.to_csv(clean_csv, index=False)

print(f"Saved {len(sunshine_clean)} rows to {clean_csv}")
print("NaN count by column:")
print(sunshine_clean.isna().sum())
assert sunshine_clean.isna().sum().sum() == 0, "NaN values still exist in cleaned output"

display(sunshine_clean)


# Cell 7
# saving Sunshine G02 to data/raw/
from pathlib import Path
import pandas as pd

file_path = r"C:\Users\samantha\Downloads\GCP_SAL22395.xlsx"
raw_g02 = pd.read_excel(file_path, sheet_name="G02", header=None, dtype=str)

project_root = Path.cwd().parent
raw_dir = project_root / "data" / "raw"
raw_dir.mkdir(parents=True, exist_ok=True)

raw_csv = raw_dir / "sunshine_G02_raw.csv"

raw_g02.to_csv(raw_csv, index=False, header=False)

print(f"Saved raw Sunshine G02 to {raw_csv}")
print(raw_g02.head())


# Cell 9
# generate and clean Brunswick G02 output (removing NaN/blank values)

import pandas as pd
from pathlib import Path

file_path = r"C:\Users\samantha\Downloads\GCP_SAL20361.xlsx"
raw_g02 = pd.read_excel(file_path, sheet_name="G02", header=None, dtype=str)

left = raw_g02[[0, 1]].rename(columns={0: "metric", 1: "value"})
right = raw_g02[[3, 4]].rename(columns={3: "metric", 4: "value"})
combined = pd.concat([left, right], ignore_index=True)

combined["metric"] = combined["metric"].str.strip()
combined["value"] = combined["value"].str.strip()
combined = combined.replace({"": pd.NA, "nan": pd.NA, "NaN": pd.NA, "NAN": pd.NA})
combined = combined.dropna(subset=["metric", "value"])

combined = combined[
    ~combined["metric"].str.contains(
        r"AUSTRALIAN BUREAU|G02 SELECTED|List of tables|sq Kms|Unnamed",
        case=False,
        na=False,
    )
]

combined["value"] = pd.to_numeric(combined["value"], errors="coerce")
brunswick_clean = combined.dropna(subset=["value"]).reset_index(drop=True)

project_root = Path.cwd().parent
clean_csv = project_root / "data" / "clean" / "brunswick_G02_clean.csv"
clean_csv.parent.mkdir(parents=True, exist_ok=True)

brunswick_clean.to_csv(clean_csv, index=False)

print(f"Saved {len(brunswick_clean)} rows to {clean_csv}")
print("NaN count by column:")
print(brunswick_clean.isna().sum())
assert brunswick_clean.isna().sum().sum() == 0, "NaN values still exist in cleaned output"

display(brunswick_clean)


# Cell 10
# saving Brunswick G02 to data/raw/
from pathlib import Path
import pandas as pd

file_path = r"C:\Users\samantha\Downloads\GCP_SAL20361.xlsx"
raw_g02 = pd.read_excel(file_path, sheet_name="G02", header=None, dtype=str)

project_root = Path.cwd().parent
raw_dir = project_root / "data" / "raw"
raw_dir.mkdir(parents=True, exist_ok=True)

raw_csv = raw_dir / "brunswick_G02_raw.csv"

raw_g02.to_csv(raw_csv, index=False, header=False)

print(f"Saved raw Brunswick G02 to {raw_csv}")
print(raw_g02.head())


# Cell 12
# generate and clean Coburg I04 output (removing NaN/blank values)

import pandas as pd
from pathlib import Path

file_path = r"C:\Users\samantha\Downloads\IP_ILOC20101503.xlsx"
raw_i04 = pd.read_excel(file_path, sheet_name="I04", header=None, dtype=str)

project_root = Path.cwd().parent
raw_dir = project_root / "data" / "raw"
clean_dir = project_root / "data" / "clean"
raw_dir.mkdir(parents=True, exist_ok=True)
clean_dir.mkdir(parents=True, exist_ok=True)

raw_csv = raw_dir / "coburg_I04_raw.csv"
clean_csv = clean_dir / "coburg_I04_clean.csv"

# saving raw Coburg I04 to data/raw/

raw_i04.to_csv(raw_csv, index=False, header=False)

pairs = []
cols = set(raw_i04.columns.tolist())
if {0, 1}.issubset(cols):
    pairs.append((0, 1))
if {3, 4}.issubset(cols):
    pairs.append((3, 4))
elif {2, 3}.issubset(cols):
    pairs.append((2, 3))

if not pairs:
    raise ValueError("Could not find expected metric/value column pairs in I04 sheet.")

frames = [
    raw_i04[[m, v]].rename(columns={m: "metric", v: "value"})
    for m, v in pairs
]
combined = pd.concat(frames, ignore_index=True)

combined["metric"] = combined["metric"].astype(str).str.strip()
combined["value"] = combined["value"].astype(str).str.strip()
combined = combined.replace({"": pd.NA, "nan": pd.NA, "NaN": pd.NA, "NAN": pd.NA})
combined = combined.dropna(subset=["metric", "value"])

combined = combined[
    ~combined["metric"].str.contains(
        r"AUSTRALIAN BUREAU|I04 SELECTED|List of tables|sq Kms|Unnamed",
        case=False,
        na=False,
    )
]

combined["value"] = pd.to_numeric(combined["value"], errors="coerce")
coburg_clean = combined.dropna(subset=["value"]).reset_index(drop=True)

coburg_clean.to_csv(clean_csv, index=False)

print(f"Saved raw Coburg I04 to {raw_csv}")
print(f"Saved {len(coburg_clean)} cleaned rows to {clean_csv}")
print("NaN count by column:")
print(coburg_clean.isna().sum())
assert coburg_clean.isna().sum().sum() == 0, "NaN values still exist in cleaned output"

display(coburg_clean.head())


# Cell 14
# merge cleaned datasets and keep only median total household income ($/weekly)

from pathlib import Path
import pandas as pd

project_root = Path.cwd()
if not (project_root / "data" / "clean").exists():
    project_root = project_root.parent
clean_dir = project_root / "data" / "clean"

target_metric = "Median total household income ($/weekly)"
files = {
    "Bundoora": "all_rows_G02_clean.csv",
    "Sunshine": "sunshine_G02_clean.csv",
    "Brunswick": "brunswick_G02_clean.csv",
    "Coburg": "coburg_I04_clean.csv",
}

rows = []
for suburb, filename in files.items():
    df = pd.read_csv(clean_dir / filename)
    metric_mask = df["metric"].astype(str).str.strip().str.casefold() == target_metric.casefold()
    match = df.loc[metric_mask, "value"]

    if match.empty:
        income_value = pd.NA
    else:
        income_value = pd.to_numeric(match.iloc[0], errors="coerce")

    rows.append(
        {
            "Suburb": suburb,
            "Median total household income ($/weekly)": income_value,
        }
    )

income_table = pd.DataFrame(rows).sort_values("Suburb").reset_index(drop=True)

display(income_table)


# Cell 15
# convert weekly household income to annual household income

weekly_col = "Median total household income ($/weekly)"
annual_col = "Annual total household income ($/year)"

annual_income_table = income_table.copy()
annual_income_table[annual_col] = pd.to_numeric(annual_income_table[weekly_col], errors="coerce") * 52
annual_income_table = annual_income_table[["Suburb", annual_col]].sort_values("Suburb").reset_index(drop=True)

# save annual income table to data/clean/

output_csv = project_root / "data" / "clean" / "annual_household_income_table.csv"
annual_income_table.to_csv(output_csv, index=False)

print(f"Saved annual income table to {output_csv}")
display(annual_income_table)


# Cell 17
from pathlib import Path
import pandas as pd

rows = [
    {"origin": "Bundoora", "destination_station": "Upfield line", "distance_km": 14.4},
    {"origin": "Sunshine", "destination_station": "Upfield line", "distance_km": 10.3},
    {"origin": "Coburg", "destination_station": "Upfield line", "distance_km": 0.0},
    {"origin": "Brunswick", "destination_station": "Upfield line", "distance_km": 0.0},
]

distance_to_upfield_df = pd.DataFrame(rows)
distance_to_upfield_df["distance_km_squared"] = (distance_to_upfield_df["distance_km"] ** 2).round(3)

project_root = Path.cwd().parent
output_path = project_root / "data" / "clean" / "bundoora_sunshine_to_upfield_driving_distances.csv"
distance_to_upfield_df.to_csv(output_path, index=False)

print(f"Saved: {output_path}")
distance_to_upfield_df


# Cell 19
# generate and clean house price data for all 4 suburbs

from pathlib import Path
import pandas as pd

project_root = Path.cwd().parent
file_path = project_root / "data" / "raw" / "houses-by-suburb-2014-2024.xlsx"

df = pd.read_excel(file_path, sheet_name="Table 1", header=None)

year_cols = {
    2015: 8,
    2016: 11,
    2017: 14,
    2018: 18,
    2019: 21,
    2020: 24,
    2021: 27,
    2022: 30,
    2023: 33,
    2024: 37,
}

suburb_names = {
    "COBURG": "Coburg",
    "BRUNSWICK": "Brunswick",
    "BUNDOORA": "Bundoora",
    "SUNSHINE": "Sunshine",
}

rows = df[df[0].astype(str).str.strip().str.upper().isin(suburb_names)].copy()
rows["Suburb"] = rows[0].astype(str).str.strip().str.upper().map(suburb_names)

house_prices = rows[["Suburb"] + [year_cols[year] for year in range(2015, 2025)]].copy()
house_prices.columns = ["Suburb"] + [str(year) for year in range(2015, 2025)]
house_prices = house_prices.reset_index(drop=True)

output_csv = project_root / "data" / "clean" / "house_prices_2015_2024.csv"
house_prices.to_csv(output_csv, index=False)

print(f"Saved {len(house_prices)} rows to {output_csv}")
display(house_prices)


# Cell 20
# generate population density tables (2018-2025) for all target suburbs

from pathlib import Path
import pandas as pd

project_root = Path.cwd()
if not (project_root / "data" / "raw").exists():
    project_root = project_root.parent

input_path = project_root / "data" / "raw" / "abs_population.xlsx"
output_dir = project_root / "data" / "clean"
output_dir.mkdir(parents=True, exist_ok=True)

# Read header rows so the year columns are correctly identified.
header_rows = pd.read_excel(input_path, sheet_name="Table 1", header=None, nrows=6)
column_names = header_rows.iloc[5, :10].tolist() + header_rows.iloc[4, 10:].tolist()

# Read the data body after header rows.
df = pd.read_excel(input_path, sheet_name="Table 1", header=None, skiprows=6)
df.columns = column_names

year_cols = [
    col for col in column_names
    if isinstance(col, (int, float)) and 2001 <= int(col) <= 2025
]

area_km2 = {
    "Sunshine": 7.3,
    "Bundoora - East": 15.0,
    "Coburg - East": 7.0,
    "Brunswick East": 5.2,
}


def normalize_file_name(name: str) -> str:
    return (
        name.lower()
        .replace(" - ", "-")
        .replace(" ", "-")
        .replace("/", "-")
        .replace("--", "-")
    )


def build_density_table(suburb_name: str, area_val: float | None):
    suburb_df = df[df["SA2 name"] == suburb_name].copy()
    if suburb_df.empty:
        raise ValueError(f"Suburb row not found: {suburb_name}")

    suburb_df[year_cols] = suburb_df[year_cols].apply(pd.to_numeric, errors="coerce")

    suburb_long = suburb_df.melt(
        id_vars="SA2 name",
        value_vars=year_cols,
        var_name="Year",
        value_name="Population",
    )

    suburb_long["Year"] = suburb_long["Year"].astype(int)
    suburb_long = suburb_long[
        (suburb_long["Year"] >= 2018) & (suburb_long["Year"] <= 2025)
    ].copy()
    suburb_long["Area_km2"] = area_val

    if area_val is not None:
        suburb_long["Density"] = suburb_long["Population"] / area_val
    else:
        suburb_long["Density"] = None
        print(f"WARNING: area_km2 is not set for {suburb_name}, density will be None.")

    return suburb_long


suburbs = ["Sunshine", "Bundoora - East", "Coburg - East", "Brunswick East"]

all_tables = []
for suburb in suburbs:
    table = build_density_table(suburb, area_km2.get(suburb))
    all_tables.append(table)

    file_name = normalize_file_name(suburb)
    target_path = output_dir / f"{file_name}_density.csv"
    table.to_csv(target_path, index=False)
    print(f"Saved {suburb} density table to {target_path}")

all_suburbs_density = pd.concat(all_tables, ignore_index=True)
combined_output_path = output_dir / "all_suburbs_density.csv"
all_suburbs_density.to_csv(combined_output_path, index=False)

print("Combined density table for all four suburbs saved to:", combined_output_path)
display(all_suburbs_density)


# Cell 21
# build a 4-row suburb summary table with key final metrics

from pathlib import Path
import pandas as pd

project_root = Path.cwd()
if not (project_root / "data" / "clean").exists():
    project_root = project_root.parent
clean_dir = project_root / "data" / "clean"

income = pd.read_csv(clean_dir / "annual_household_income_table.csv")
distance = pd.read_csv(clean_dir / "bundoora_sunshine_to_upfield_driving_distances.csv")
density = pd.read_csv(clean_dir / "all_suburbs_density.csv")
density["Year"] = pd.to_numeric(density["Year"], errors="coerce").astype("Int64")
density = density.rename(columns={"SA2 name": "Suburb"})
density["Suburb"] = density["Suburb"].replace(
    {
        "Bundoora - East": "Bundoora",
        "Brunswick East": "Brunswick",
        "Coburg - East": "Coburg",
    }
)
house_prices = pd.read_csv(clean_dir / "house_prices_2015_2024.csv")

density_2025 = (
    density[density["Year"] == 2025][["Suburb", "Density"]]
    .drop_duplicates(subset=["Suburb"])
    .rename(columns={"Density": "Population Density (2025 only)"})
)

income_summary = income.rename(
    columns={"Annual total household income ($/year)": "Household Average Income per year"}
)

distance_summary = distance[["origin", "distance_km"]].rename(
    columns={"origin": "Suburb", "distance_km": "Distance to Upfield Line (km)"}
)

house_price_cols = ["Suburb"] + [str(year) for year in range(2015, 2025)]
house_price_summary = house_prices[house_price_cols].rename(
    columns={str(year): f"Housing Price {year}" for year in range(2015, 2025)}
)

combined_table = (
    income_summary.merge(density_2025, on="Suburb", how="left")
    .merge(distance_summary, on="Suburb", how="left")
    .merge(house_price_summary, on="Suburb", how="left")
)

combined_table = combined_table[
    [
        "Suburb",
        "Household Average Income per year",
        "Population Density (2025 only)",
        "Distance to Upfield Line (km)",
        "Housing Price 2015",
        "Housing Price 2016",
        "Housing Price 2017",
        "Housing Price 2018",
        "Housing Price 2019",
        "Housing Price 2020",
        "Housing Price 2021",
        "Housing Price 2022",
        "Housing Price 2023",
        "Housing Price 2024",
    ]
].sort_values(["Suburb"]).reset_index(drop=True)

output_csv = clean_dir / "suburb_summary_table.csv"
combined_table.to_csv(output_csv, index=False)

print(f"Saved combined table to {output_csv}")
display(combined_table)