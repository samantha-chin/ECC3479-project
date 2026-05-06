# ECC3479 Notebook README

This document is specific to [ECC3479_notebook.ipynb](ECC3479_notebook.ipynb) and is intentionally separate from the exploratory analysis README for [EDA.ipynb](EDA.ipynb).

## Overview

This notebook cleans and standardizes house price and population density data for all 57 Melbourne suburbs over the 2015–2024 period. It serves as the primary data preparation layer for the project's analysis.

The notebook handles data import, cleaning, standardization, and export in both wide (suburb × year matrix) and long (suburb-year observation) formats.

It also includes a Daniel Bowen level-crossings classification step that builds treated and untreated suburb tables using only the `Suburbs` and `Status 11/2022` columns from the November 2022 update page.

## Purpose

To produce clean, consistent, and analysis-ready datasets for:
- House price trends across all suburbs (2015–2024)
- Population density changes across all suburbs (2015–2024)

These cleaned datasets form the foundation for exploratory data analysis and causal modelling downstream.

## Scope of Data Cleaning

The notebook processes two main datasets:

### House Prices
- Cleans raw house price data for all 57 suburbs
- Handles currency formatting, missing values, and duplicate entries
- Converts prices to numeric format
- Produces wide-format output (one row per suburb, columns for each year)

### Population Density
- Cleans density data from 2015–2024
- Standardizes suburb names and numeric fields
- Retains supporting fields (population, area, SA2 components)
- Produces both wide-format (density as pivot) and long-format outputs

## What ECC3479_notebook.ipynb Does

### Data Import
- Loads raw house price data from `data/raw/closest_lxrp_site_house_prices_2015_2024.csv`
- Loads cleaned population density data from `data/clean/requested_suburbs_density_2015_2024_long.csv`

### Data Cleaning—House Prices
- Renames columns to lowercase for consistency
- Standardizes suburb names (strip whitespace, title case)
- Removes currency symbols and commas from price columns
- Converts price columns to numeric type, then integer
- Drops incomplete rows and duplicates (keeps first occurrence)
- Sorts alphabetically by suburb
- Validates data consistency

### Data Cleaning—Population Density
- Renames columns to lowercase for consistency
- Standardizes suburb names (strip whitespace, title case)
- Converts numeric fields to proper types
- Filters to 2015–2024 only
- Rounds density to 2 decimal places
- Removes duplicate suburb-year combinations
- Keeps relevant columns: suburb, year, density, population, area, SA2 components

### Output Generation
- **House prices wide format**: `data/clean/all_suburbs_house_prices_2015_2024.csv`
  - One row per suburb, columns for each year (2015–2024)
  - 57 suburbs, 11 year columns
  
- **Population density wide format**: `data/clean/all_57_suburbs_population_density_2015_2024.csv`
  - One row per suburb, columns for each year (2015–2024)
  - 57 suburbs, 11 year columns

### Daniel Bowen Classification
- Loads the November 2022 level-crossings update page from Daniel Bowen’s website
- Extracts only the `Suburbs` / `Suburb` and `Status 11/2022` columns from the table
- Classifies suburbs as treated when the status is `Completed`, `Planning`, or `Underway`
- Leaves road names out of the treated and untreated suburb tables

### Diagnostics
- Prints cleaning summary (number of suburbs, missing values, duplicates)
- Displays full cleaned datasets for visual inspection
- Lists all suburb names for reference

## Key Data Used

### Input Files
- `data/raw/closest_lxrp_site_house_prices_2015_2024.csv` — Raw house prices
- `data/clean/requested_suburbs_density_2015_2024_long.csv` — Cleaned density (long format)

### Output Files
- `data/clean/all_suburbs_house_prices_2015_2024.csv` — Clean house prices (wide format)
- `data/clean/all_57_suburbs_population_density_2015_2024.csv` — Clean density (wide format)

## How To Run ECC3479

1. Open [ECC3479_notebook.ipynb](ECC3479_notebook.ipynb) in VS Code or Jupyter.
2. Install dependencies (or use the project virtual environment):

```bash
pip install pandas numpy jupyter
```

3. Run cells from top to bottom:
   - First cell processes house prices and saves the wide-format output
   - Second cell processes population density and saves the wide-format output
   - Cells display full datasets for verification

4. Check output files in `data/clean/` to confirm both wide-format CSVs were created.

## Notes on Data Handling

- **Suburb Name Standardization**: All suburb names are converted to title case and stripped of extra whitespace to ensure consistency across the project.
- **Missing Values**: Rows with missing suburb names or no price/density data for any year are dropped during cleaning.
- **Duplicates**: When duplicate suburb entries appear, only the first occurrence is retained.
- **Year Range**: Density data is explicitly filtered to 2015–2024; any rows outside this range are excluded.
- **Format Consistency**: Output files use lowercase column names and numeric data types to facilitate downstream analysis.
- **Wide vs. Long Format**: This notebook produces wide-format files for convenience; long-format alternatives are available in the source data or can be pivoted as needed.
- **Daniel Bowen Table Parsing**: The treatment classification is suburb-only and status-only; road names are not used in the treated or untreated tables.
