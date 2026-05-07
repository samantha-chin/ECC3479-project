# EDA Visualisation README

### Overview

EDA Visualisation.ipynb contains the exploratory data analysis (EDA) and visualisation work for the project. The notebook combines cleaned house price data, treatment classifications, and population density data to explore relationships between Melbourne suburbs affected by the Suburban Rail Loop (treated suburbs) and comparison suburbs (untreated suburbs).

The notebook focuses on identifying trends, distributional differences, and potential relationships between house prices and population density over time.

### Purpose

The purpose of this notebook is to:

- Explore patterns in house prices and population density across suburbs
- Compare treated and untreated suburbs over time
- Prepare data for later econometric analysis
- Check whether the treatment and control groups display different trends
- Produce visual evidence connected to the project’s research question
- Conduct diagnostic and correlation checks before formal modelling

The notebook is primarily designed for exploratory analysis and interpretation rather than causal estimation.

### Treated And Untreated House Price Files

The matched house price data is merged with the Daniel Bowen treatment classification.

This produces:

- data/clean/house_prices_treated_suburbs.csv
- data/clean/house_prices_untreated_suburbs.csv

### Current output size:

- 24 treated suburbs
- 25 untreated suburbs
- Combined Analysis Dataset

The project also creates:

- `data/clean/population_density_all_suburbs.csv`

This file combines:

- Suburb name
- House prices from 2015–2024
- Project status
- Treatment indicator
- Population values from 2015–2024

Current output size:

- 49 combined analysis rows

### What EDA Visualisation.ipynb Does

The notebook performs the following tasks:

Loads cleaned house price and population density datasets
Labels suburbs as treated or untreated
Normalises suburb names before merging datasets
Converts house prices into log house prices
Reshapes wide-format house price data into suburb-year long format
Merges house price and density data into a panel-style dataset
Creates grouped yearly median summaries
Creates log_Density for correlation and diagnostic analysis
Produces exploratory charts and statistical diagnostic plots
Adds written interpretation for each visualisation

### The notebook uses cleaned files such as:

`data/clean/house_prices_treated_suburbs.csv`
`data/clean/house_prices_untreated_suburbs.csv`
`data/clean/requested_suburbs_density_2015_2024_long.csv`

The exploratory notebook currently includes:

- Ranked lollipop chart of median log house price by suburb from 2015–2024
- Box-and-whisker plot comparing treated, untreated, and all suburb house price distributions
- Boxplot of population density across suburb-year observations
- Time-series plot of median log house prices for treated and untreated suburbs
- Time-series plot of overall median population density
- Scatter plot of log house price against population density
- Correlation heatmap for house prices, density, year, and log density
- Between-suburb versus within-suburb comparison
- OLS residuals-versus-fitted plot
- OLS Q-Q plot for standardised residuals

Each graph includes written interpretation connected to the research question.

### How To Run

Install the required Python packages before running the notebook:

pip install pandas numpy matplotlib seaborn statsmodels
Running The Notebook
Open the project folder in Jupyter Notebook or VS Code.

Navigate to:

EDA Visualisation.ipynb

Ensure the required cleaned datasets exist inside:

data/clean/
Run the notebook cells sequentially from top to bottom.
Expected Inputs

The notebook expects the following cleaned datasets to already exist:

- `data/clean/house_prices_treated_suburbs.csv`
- `data/clean/house_prices_untreated_suburbs.csv`
- `data/clean/requested_suburbs_density_2015_2024_long.csv`

Running the notebook will generate:

- Exploratory visualisations
- Summary statistics
- Correlation diagnostics
- Regression diagnostic plots
- Combined panel-style datasets used for analysis and interpretation

These outputs are used to support later econometric modelling and discussion throughout the project.
## Visualisation Work

The visualisation work is in `visualisations.ipynb`.

It uses cleaned files such as:

- `data/clean/house_prices_treated_suburbs.csv`
- `data/clean/house_prices_untreated_suburbs.csv`
- `data/clean/requested_suburbs_density_2015_2024_long.csv`

The notebook:

- Labels suburbs as treated or untreated
- Normalises suburb names before merging
- Converts house prices into log house prices
- Reshapes wide house price data into suburb-year long format
- Merges house price and density data into a panel-style dataset
- Creates grouped yearly medians
- Creates `log_Density` for correlation and diagnostic checks

