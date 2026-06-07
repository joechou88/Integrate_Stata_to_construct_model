## Python Scripts
#### 1-1. Integrate SDC data (`merge_SDC.py`)
- **Objective**: combine SDC data (Excel) with Financial Lease data (Stata)
- **Input**: `Stata/Financial_npv_lease20152024.dta`, `Input/Calculated_All_countries_SDC_2015-2024.xlsx`
- **Output**: `Stata/IPO_2015_2024.dta`
#### 1-2. Integrate country-level controls data (`merge_country_level_controls.py`)
- **Objective**: Merge the data with country-level controls (from Excel) matching year t to year t, as contemporaneous macroeconomic conditions and market sentiment directly impact underwriter pricing during the issue year.
- **Input**: `Stata/IPO_2015_2024.dta`, `Input/country_controls.xlsx`
- **Output**: `Stata/IPO_2015_2024_with_country_level_controls.dta`
- **Problem**: In 2021, The Heritage Foundation removed Hong Kong from its independent rankings, merging its economic freedom score with China's, citing Beijing's control over Hong Kong's economic policies. (Source: https://www.bbc.com/zhongwen/trad/business-56277534)
- **Solution**: Macroeconomic freedom is highly "rigid" and rarely mutates in the short term. To avoid data distortion caused by the extreme score gap between China and Hong Kong (approx. 50 vs. 90), Hong Kong's 2020 score was directly applied to the 2021–2024 Hong Kong IPO samples.
#### 1-3. Integrate Financial Analyst Forecast data (`AFOL.py`)
- **Objective**: Merge the data with AFOL (from SAS) matching year t to year t, using primary key `country_code` + `fpe_year`
- **Input**: `Input/ibes_non_us_1983_2025.sas7bdat`, `Input/ibes_us_1983_2025.sas7bdat`, `Stata/IPO_2015_2024_with_country_level_controls.dta`
- **Output**: `Stata/IPO_2015_2024_with_AFOL.dta`
#### 1-4. Integrate Institutional Ownership data (`INST.py`)
- **Objective**: Merge the data with INST (from ) matching year t to year t-1
- **Input**: `Input/`
- **Output**: `Stata/IPO_2015_2024_with_INST.dta`
#### 2. Derive variables (`derive_columns_in_stata.py`)
- **Objective**: 
    - create new variable `Post` based on existing variable `year` in Stata
    - create new variable `Postxhigh_lease` based on the above `Post` and existing variable `high_lease` in Stata
- **Input**: `Stata/IPO_2015_2024_with_INST.dta`
- **Output**: `Stata/IPO_2015_2024_with_post_and_interation.dta`
#### 3-1. Calculate Market_Return and Market_Volatility (`market_return.py`)
- **Objective**: calculate variables below
    - Market_Return: Natural log of 1 plus the market return in that country in the 90 trading days before `Dates: Issue Date`.
    - Market_Volatility: The standard deviation of the market index return over the 21 trading days ( −21, −1) before `Dates: Issue Date`.
- **Input**: `Input/compustat_market_price_2015_2024_with_country_code.csv`, `Stata/IPO_2015_2024_with_post_and_interation.dta`
- **Output**: `Stata/IPO_2015_2024_with_market_return_and_volatility.dta`
#### 3-2. Calculate IPO Underpricing (`security_price.py`)
- **Objective**: calculate variables below
    - Underpricing: First-day market closing price of an IPO minus its `Offer Price (USD)`, scaled by `Offer Price (USD)`.
- **Input**: `Input/compustat_security_daily_price_2015_2024.csv`, `Stata/IPO_2015_2024_with_market_return_and_volatility.dta`
- **Output**: `Stata/IPO_2015_2024_with_IPO_Underpricing.dta`
#### 4. Column Filtering (`filter.py`)
- **Objective**: drop unnecessary variables for model 1
- **Input**: `Stata/IPO_2015_2024_with_IPO_Underpricing.dta`
- **Output**: `Stata/IPO_2015_2024_filtered.dta`