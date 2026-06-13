## Python Scripts
#### 1-1. Integrate SDC data (`merge_SDC.py`)
- **Objective**: combine SDC data (Excel) with Financial Lease data (Stata), keeping all SDC records instead of dropping unmatched rows.
- **Input**: `Stata/Financial_npv_lease20152024.dta`, `Input/Calculated_All_countries_SDC_2015-2024.xlsx`
- **Output**: `Stata/IPO_2015_2024.dta`
- **Sample size**: 4,818 -> 3,111 
#### 1-2. Integrate country-level controls data (`merge_country_level_controls.py`)
- **Objective**: Merge the data with country-level controls (from Excel) matching year t to year t, as contemporaneous macroeconomic conditions and market sentiment directly impact underwriter pricing during the issue year.
- **Input**: `Stata/IPO_2015_2024.dta`, `Input/country_controls.xlsx`
- **Output**: `Stata/IPO_2015_2024_with_country_level_controls.dta`
- **Problem**: In 2021, The Heritage Foundation removed Hong Kong from its independent rankings, merging its economic freedom score with China's, citing Beijing's control over Hong Kong's economic policies. (Source: https://www.bbc.com/zhongwen/trad/business-56277534)
- **Solution**: Macroeconomic freedom is highly "rigid" and rarely mutates in the short term. To avoid data distortion caused by the extreme score gap between China and Hong Kong (approx. 50 vs. 90), Hong Kong's 2020 score was directly applied to the 2021–2024 Hong Kong IPO samples.
- **Sample size**: 3,111 -> 3,110
#### 1-3. Integrate Financial Analyst Forecast data (`AFOL.py`)
- **Objective**: Merge the data with average AFOL (from SAS) matching year t to year t, using primary key `country_code` + `fpe_year`.
- **Input**: `Input/ibes_non_us_1983_2025.sas7bdat`, `Input/ibes_us_1983_2025.sas7bdat`, `Stata/IPO_2015_2024_with_country_level_controls.dta`
- **Output**: `Stata/IPO_2015_2024_with_AFOL.dta`
- **Memo**: `AFOL` is considered as country-level control instead of firm-level control since financial analysts typically do not immediately release earnings forecasts at the time of an IPO, thus there should be no `AFOL` data for that firm in that year.
- **Sample size**: 3,110 -> 3,110
#### 1-4. Integrate Institutional Ownership data (`INST.py`)
- **Objective**: Merge the data with INST (from SAS) by forward-matching the IPO `Issue_Date` to the nearest subsequent quarter-end (`qtrdate`) within 180 days.
- **Missing Value Rule**:
  | Missing Status | Interpretation | Action |
  | :--- | :--- | :--- |
  | Missing `valueheld`, but `price`, `shrout` present | This company is covered by LSEG Global Ownership, but no institutional investors have reported holdings | Substitute`INST` with 0 |
  | Missing `price` or `shrout` / Missing SEDOL | This company is not covered by LSEG Global Ownership | Drop the sample |
- **Input**: `Input/INST/inst_1997_2025.sas7bdat`, `Stata/IPO_2015_2024_with_AFOL.dta`
- **Output**: `Stata/IPO_2015_2024_with_INST.dta`
- **Sample size**: 3,110 -> 1,184 (55 missing SEDOL; 1,129 missing price or shrout)
#### 2. Derive variables (`derive_columns_in_stata.py`)
- **Objective**: 
    - create new variable `Post` based on existing variable `year` in Stata
    - create new variable `Postxhigh_lease` based on the above `Post` and existing variable `high_lease` in Stata
- **Input**: `Stata/IPO_2015_2024_with_INST.dta`
- **Output**: `Stata/IPO_2015_2024_with_post_and_interation.dta`
#### 3-1. Calculate Market_Return and Market_Volatility (`market_price.py`)
- **Objective**: calculate variables below
    - Market_Return = ln(P<sub>t-1</sub> / P<sub>t-91</sub>), where:
      - P<sub>t-1</sub> = market closing price one trading day before `Issue_Date` t  
      - P<sub>t-91</sub> = market closing price 91 trading days before `Issue_Date` t 
    - Market_Volatility = StdDev(r<sub>t-21</sub>, ..., r<sub>t-1</sub>), where r<sub>t-n</sub> = market return n day before `Issue Date` t, calculated as (P<sub>t</sub> - P<sub>t-1</sub>) / P<sub>t-1</sub>
- **Input**: `Input/compustat_market_price_2015_2024_with_country_code.csv`, `Stata/IPO_2015_2024_with_post_and_interation.dta`
- **Output**: `Stata/IPO_2015_2024_with_market_return_and_volatility.dta`
- **Sample size**:  -> 
#### 3-2. Calculate IPO Underpricing (`security_price.py`)
- **Objective**: calculate variables below
    - Underpricing = (P<sub>t</sub> - P<sub>offer</sub>) / P<sub>offer</sub>, where:
      - P<sub>t</sub> = the first valid market closing price (from Compustat) of an IPO within a $[-3, +60]$ day window around the `Issue_Date` t (from SDC), prioritizing the exact issue date, followed by the closest subsequent day, and lastly the closest preceding day.
      - P<sub>offer</sub> = `Offer_Price_USD` of the IPO (from SDC)
- **Input**: `Input/compustat_security_daily_price_2015_2024.csv`, `Stata/IPO_2015_2024_with_market_return_and_volatility.dta`
- **Output**: `Stata/IPO_2015_2024_with_IPO_Underpricing.dta`
- **Sample size**:  -> 
#### 4. Column Filtering (`filter.py`)
- **Objective**: drop unnecessary variables for model 1
- **Input**: `Stata/IPO_2015_2024_with_IPO_Underpricing.dta`
- **Output**: `Stata/IPO_2015_2024_filtered.dta`
