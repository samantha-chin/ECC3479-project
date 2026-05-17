# DiD Regression Table

This repository contains the complete pipeline for analyzing the causal effect of the Level Crossing Removal Project (LXRP) on house prices in Melbourne suburbs using a Difference-in-Differences (DiD) approach.

## Analysis Declaration

This is a **causal analysis** aiming to identify the treatment effect of LXRP on house prices. The main DiD regression in `DID Regression Table.ipynb` uses 2017 as the post-treatment milestone. The current estimate for the Treat x Post effect is small and statistically insignificant, consistent with no clear post-2017 price impact in treated suburbs once fixed effects and population controls are included.

## Parallel Trends Test

The notebook also performs an event-study based parallel-trends test. It estimates relative-year treatment coefficients for treated suburbs around 2017, using 2016 as the reference pre-treatment year, while controlling for log population, suburb fixed effects, and year fixed effects. The event-study output is saved to `results/event_study_table.csv`, `results/event_study_table.html`, `results/event_study_plot.png`, and `results/event_study_plot.pdf`.

## Repository Pipeline and Reproduction

The full pipeline from raw data to results is reproducible by following these steps. All code is in Python with required packages listed in `requirements.txt` (if not present, install via pip).

### Prerequisites
- Python 3.8+
- Required packages: pandas, numpy, statsmodels, openpyxl (for Excel reading)

### Step 1: Data Cleaning
Run the data processing scripts to generate clean datasets:

1. **Population Density Processing**:
   - Execute `ECC3479_combined.ipynb` or `code/clean_population.py`
   - Input: `data/raw/abs_population.xlsx`
   - Output: `data/clean/population_density_all_suburbs.csv`, etc.

2. **Household Income Processing**:
   - Part of `ECC3479_combined.ipynb`
   - Input: Raw ABS exports in `data/raw/`
   - Output: `data/clean/annual_household_income_table.csv`

3. **Distance and House Prices**:
   - Execute `ECC3479_combined.ipynb`
   - Output: `data/clean/house_prices_2015_2024.csv`, distance tables

4. **Matching and Panel Creation**:
   - Run `code/eda_notebook_script.py` or relevant notebooks
   - Output: `data/clean/matched_houses_population_2015_2024_prices.csv`, `matched_houses_population_2015_2024_population.csv`

### Step 2: Analysis
Execute the primary analysis notebook:
- File: `primary econometric analysis.ipynb`
- This runs the DiD regression and generates results
- Output: Regression tables in `results/` (e.g., `did_regression_table_final.csv`)

### Step 3: Results and Visualizations
- Additional notebooks: `DID Regression Table.ipynb`, `EDA Visualisation.ipynb`, `visualisations.ipynb`
- Generate plots and formatted tables in `results/`

### Running the Pipeline
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt` (create if missing)
3. Run notebooks in order: data cleaning first, then analysis
4. Results will be saved to `results/` folder

## Project Structure
- `data/raw/`: Raw input files
- `data/clean/`: Processed datasets
- `code/`: Python scripts
- `results/`: Output tables and figures
- Notebooks: `.ipynb` files for interactive analysis
- `README.md`: This file

## Methods and Tools
- Data processing: pandas, openpyxl
- Analysis: statsmodels for OLS regression
- Visualization: matplotlib, seaborn (in visualization notebooks)
- Methods chosen for appropriateness to causal inference in panel data

Final Combined Tables
The notebook ends by merging the cleaned final tables into analysis-ready combined outputs:

suburb_year_combined_table_2015_2024.csv: Suburb-year format combining income, distance, house prices, and available density values.
suburb_summary_table.csv: Four-row summary (Brunswick, Bundoora, Coburg, Sunshine) with:
Household Average Income per year
Population Density (2025 only)
Distance to Upfield Line (km)
Housing Price 2014 through Housing Price 2024
Note: Housing Price 2014 is currently blank because the cleaned house-price source in this repository starts at 2015.

Output Files
Generated files are written to data/clean and include:

all_rows_G02_clean.csv
sunshine_G02_clean.csv
brunswick_G02_clean.csv
coburg_I04_clean.csv
annual_household_income_table.csv
bundoora_sunshine_to_upfield_driving_distances.csv
house_prices_2015_2024.csv
sunshine_density.csv
bundoora-east_density.csv
brunswick-east_density.csv
coburg-east_density.csv
all_suburbs_density.csv
suburb_year_combined_table_2015_2024.csv
suburb_summary_table.csv
Requirements
Use Python 3.10 or newer.

Install the notebook dependencies with:

pip install pandas openpyxl jupyter
How To Run
Open ECC3479_combined.ipynb in VS Code or Jupyter.
Make sure the source workbooks referenced in the notebook are available locally.
Run the notebook from top to bottom.
Check data/clean for the generated CSV outputs.
Notes
Some notebook cells still contain absolute paths from the original author machine. Update those paths if the referenced source files are stored elsewhere.
The population-density calculations use fixed suburb areas in square kilometres.
Rerunning the notebook will overwrite existing output CSV files in data/clean.