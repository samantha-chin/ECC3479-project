# ECC3479 Project

This repository centres on a single combined analysis notebook, which prepares suburb-level data for income, population density, distance, house-price analysis as well as a summary table at the end.

The notebook reads source files from `data/raw` and writes analysis-ready CSV files to `data/clean`.

## Project Layout

- [ECC3479_combined.ipynb](ECC3479_combined.ipynb) - combined notebook for population density, income, distance, and house-price processing
- [code/notebook_compiled.py](code/notebook_compiled.py) - script version of the notebook workflow
- [code/clean_population.py](code/clean_population.py) - script used for the population-density processing
- [data/raw](data/raw) - raw CSV and workbook inputs
- [data/clean](data/clean) - cleaned CSV outputs

## What The Notebook Does

### Population Density

The first part of the notebook builds population density tables for four suburbs:

- Sunshine
- Bundoora - East
- Brunswick East
- Coburg - East

It:

1. Reads ABS population data from `abs_population.xlsx`.
2. Reconstructs the year columns from the workbook header rows.
3. Filters each suburb and reshapes the data into long format.
4. Keeps the 2018-2025 period.
5. Adds fixed suburb land areas and calculates `Density = Population / Area_km2`.
6. Saves one CSV per suburb plus a combined density table.

### Household Income

The income section cleans ABS G02 and I04 tables for Bundoora, Sunshine, Brunswick, and Coburg.

It:

1. Reads the raw ABS exports.
2. Removes blank rows, header noise, and non-numeric values.
3. Saves cleaned suburb-level tables.
4. Extracts `Median total household income ($/weekly)` for each suburb.
5. Converts weekly household income to annual income using a 52-week year.
6. Saves `annual_household_income_table.csv`.

### Distance To Upfield

The notebook also creates a small distance table from Bundoora and Sunshine to the Upfield line.

It stores:

- `distance_km`
- `distance_km_squared`

The notebook notes that these distances were entered manually from Google Maps.

### House Prices

The final section extracts house prices for the 2015-2024 period and saves them to `house_prices_2015_2024.csv`.

### Final Combined Tables

The notebook ends by merging the cleaned final tables into analysis-ready combined outputs:

1. `suburb_year_combined_table_2015_2024.csv`:
Suburb-year format combining income, distance, house prices, and available density values.
2. `suburb_summary_table.csv`:
Four-row summary (Brunswick, Bundoora, Coburg, Sunshine) with:
- `Household Average Income per year`
- `Population Density (2025 only)`
- `Distance to Upfield Line (km)`
- `Housing Price 2014` through `Housing Price 2024`

Note: `Housing Price 2014` is currently blank because the cleaned house-price source in this repository starts at 2015.

## Output Files

Generated files are written to `data/clean` and include:

- `all_rows_G02_clean.csv`
- `sunshine_G02_clean.csv`
- `brunswick_G02_clean.csv`
- `coburg_I04_clean.csv`
- `annual_household_income_table.csv`
- `bundoora_sunshine_to_upfield_driving_distances.csv`
- `house_prices_2015_2024.csv`
- `sunshine_density.csv`
- `bundoora-east_density.csv`
- `brunswick-east_density.csv`
- `coburg-east_density.csv`
- `all_suburbs_density.csv`
- `suburb_year_combined_table_2015_2024.csv`
- `suburb_summary_table.csv`

## Requirements

Use Python 3.10 or newer.

Install the notebook dependencies with:

```bash
pip install pandas openpyxl jupyter
```

## How To Run

1. Open [ECC3479_combined.ipynb](ECC3479_combined.ipynb) in VS Code or Jupyter.
2. Make sure the source workbooks referenced in the notebook are available locally.
3. Run the notebook from top to bottom.
4. Check `data/clean` for the generated CSV outputs.

## Notes

- Some notebook cells still contain absolute paths from the original author machine. Update those paths if the referenced source files are stored elsewhere.
- The population-density calculations use fixed suburb areas in square kilometres.
- Rerunning the notebook will overwrite existing output CSV files in `data/clean`.
