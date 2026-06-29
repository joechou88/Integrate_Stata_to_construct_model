## Python Scripts
#### 0-2. Lag Firm Characteristics Controls (`0-2_lag_variables_in_stata.py`)
- **Objective**: generate lagged variables for the Financial Lease data (Stata) and merge them back into the original dataset.
- **Input**: `Stata/Financial_npv_lease20152024_0621.dta`
- **Output**: `Stata/Financial_npv_lease20142024_lag_variables_0621.dta`
- **Detailed updates**:
  - ln_sales_lag      : 538258/596812 updated successfully
  - capex_at_lag      : 400458/596812 updated successfully
  - capex_sales_lag   : 400458/596812 updated successfully
  - rd_at_lag         : 538258/596812 updated successfully
  - rd_sales_lag      : 538258/596812 updated successfully
  - roa_ebitda_lag    : 519304/596812 updated successfully
  - lev_lag           : 538258/596812 updated successfully
  - abs_abacc_lag     : 365326/596812 updated successfully
  - total_assets_lag  : 538258/596812 updated successfully
#### 1-1. Integrate SDC data (`1-1_merge_SDC.py`)
- **Objective**: combine SDC data (Excel) with Financial Lease data (Stata), using primary key `dscd`, `isin`, or `sedol`. We keep all SDC records instead of dropping unmatched rows.
- **Input**: `Input/Calculated_All_countries_SDC_2015-2019.xlsx`, `Stata/Financial_npv_lease20142024_lag_variables_0621.dta`, `Input/country_code.xlsx`
- **Output**: `Stata/IPO_2015_2019_0621.dta`
- **Match result**: A total of 2,344 rows were exported. This includes 1,926 successful matches, along with 418 unmapped rows.
#### 1-2. Convert USD to local currency (`1-2_offer_price_from_USD_to_local.py`)
- **Objective**: convert the USD offer price to local currency by merging the SDC data (Stata) with country-specific currency codes (Excel) and daily exchange rate data (CSV), using country code and issue date as primary key.
- **Input**: `Input/Compustat/global_exchange_rate_2015_2024.csv`, `Stata/Financial_npv_lease20142024_lag_variables_0621.dta`, `Input/country_code_with_curd.xlsx`
- **Output**: `Stata/IPO_2015_2019_with_updated_offer_price_0621.dta`
#### 1-3. Integrate country-level controls data (`merge_country_level_controls.py`)
- **Objective**: Merge the data with country-level controls (from Excel) matching year t to year t, as contemporaneous macroeconomic conditions and market sentiment directly impact underwriter pricing during the issue year. We also divide the original `CAP_Ratio` by 100 and apply a natural logarithm transformation: `CAP_Ratio = ln(CAP_Ratio / 100)`
- **Problem**: In 2021, The Heritage Foundation removed Hong Kong from its independent rankings, merging its economic freedom score with China's, citing Beijing's control over Hong Kong's economic policies. (Source: https://www.bbc.com/zhongwen/trad/business-56277534)
- **Solution**: Macroeconomic freedom is highly "rigid" and rarely mutates in the short term. To avoid data distortion caused by the extreme score gap between China and Hong Kong (approx. 50 vs. 90), Hong Kong's 2020 score was directly applied to the 2021–2024 Hong Kong IPO samples.
- **Input**: `Stata/IPO_2015_2019_with_updated_offer_price_0621.dta`, `Input/country_controls.xlsx`
- **Output**: `Stata/IPO_2015_2019_with_country_level_controls_0621.dta`
- **Match result**: A total of 2,344 rows were exported. This includes 2,340 successful matches, along with 4 unmapped rows.
#### 1-4. Integrate Financial Analyst Forecast data (`AFOL.py`)
- **Objective**: Merge the data with total AFOL (from SAS) matching year t to year t, using primary key `country_code` + `fpe_year`.
- **Memo**: `AFOL` is considered as country-level control instead of firm-level control since financial analysts typically do not immediately release earnings forecasts at the time of an IPO, thus there should be no `AFOL` data for that firm in that year.
- **Input**: `Input/ibes_non_us_1983_2025.sas7bdat`, `Input/ibes_us_1983_2025.sas7bdat`, `Input/ibes_int_1983_2025.sas7bdat`, `Stata/IPO_2015_2019_with_country_level_controls_0621.dta`
- **Output**: `Stata/IPO_2015_2019_with_AFOL_0621.dta`
- **Match result**: A total of 2,344 rows were exported. This includes 2,344 successful matches, along with 0 unmapped rows.
#### 1-5. Integrate Institutional Ownership data (`INST.py`)
- **Objective**: Merge the data with INST (from SAS) by forward-matching the IPO `Issue_Date` to the nearest subsequent quarter-end (`qtrdate`) within 180 days. We prioritize the nearest quarter-end where `valueheld`, `price`, and `shrout` are all simultaneously observable.
- **Missing Value Rule**:
  | Missing Status | Interpretation | Action |
  | :--- | :--- | :--- |
  | Missing `valueheld`, but `price`, `shrout` present | This company is covered by LSEG Global Ownership, but no institutional investors have reported holdings | Substitute`INST` with 0 |
  | Missing `price` or `shrout` / Missing SEDOL | This company is not covered by LSEG Global Ownership | Drop the sample |
- **Input**: `Input/INST/inst_1997_2025.sas7bdat`, `Stata/IPO_2015_2019_with_AFOL_0621.dta`
- **Output**: `Stata/IPO_2015_2019_with_INST_0621.dta`
- **Match result**: A total of 2,344 rows were exported. This includes 2,230 successful matches, along with 114 unmapped rows.
#### 1-6. Integrate SME_IFRS_adoption data (`1-6_SME_IFRS_adoption.py`)
- **Objective**: Merge the data with SME IFRS adoption data (from Excel), using country code as primary key.
- **Input**: `Input/SME_IFRS_adoption.xlsx`, `Stata/IPO_2015_2019_with_INST_0621.dta`
- **Output**: `Stata/IPO_2015_2019_with_SME_IFRS_adoption_0621.dta`
#### 2-1. Derive variables (`2-1_derive_columns_in_stata.py`)
- **Objective**: 
    - create new variable `Post` based on existing variable `year` in Stata
    - create new variable `Postxlease_intensity_pre` based on the above `Post` and existing variable `lease_intensity_pre` in Stata
- **Input**: `Stata/IPO_2015_2019_with_SME_IFRS_adoption_0621.dta`
- **Output**: `Stata/IPO_2015_2019_derive_columns_0621.dta`
#### 2-2. Calculate Relative_Offer_Size (`2-2_Relative_Offer_Size.py`)
- **Input**: `Stata/IPO_2015_2019_derive_columns_0621.dta`
- **Output**: `Stata/IPO_2015_2019_with_relative_offer_size_0621.dta`
#### 3-1. Calculate Market_Return and Market_Volatility (`market_price.py`)
- **Objective**: calculate variables below
    - Market_Return = ln(P<sub>t-1</sub> / P<sub>t-91</sub>), where:
      - P<sub>t-1</sub> = market closing price one trading day before `Issue_Date` t  
      - P<sub>t-91</sub> = market closing price 91 trading days before `Issue_Date` t 
    - Market_Volatility = StdDev(r<sub>t-21</sub>, ..., r<sub>t-1</sub>), where r<sub>t-n</sub> = market return n day before `Issue Date` t, calculated as (P<sub>t</sub> - P<sub>t-1</sub>) / P<sub>t-1</sub>
- **Problem**: We should use `Stock Index` listed in Worldscope definition. If the exact `Stock Index` cannot be found in Compustat dataset, we select the best available alternative from the existing indices, prioritizing those used in prior literature or those offering broader market coverage.
  | Country | Worldscope listed Stock Index | Best available alternative |
  | :--- | :--- | :--- |
  | Canada | S&P/TSX Composite Index | MSCI - Canada Index |
  | Columbia | IGBC Index | FTSE World Index - Colombia |
  | Italy | FTSE Italia All Share | BCI All-Share Index |
  | Norway | Oslo Bors Benchmark Index | OSE All Share Index |
- **Input**: `Input/Compustat/global_market_price_2014_2024_with_country_code.csv`, `Stata/IPO_2015_2019_with_relative_offer_size_0621.dta`
- **Output**: `Stata/IPO_2015_2019_with_market_return_and_market_volatility_0621.dta`
- **Match result**: A total of 2,344 rows were exported. This includes 2,344 successful matches, along with 0 unmapped rows.
#### 3-2. Calculate IPO Underpricing (`security_price.py`)
- **Objective**: calculate variables below
    - Underpricing = (P<sub>t</sub> - P<sub>offer</sub>) / P<sub>offer</sub>, where:
      - P<sub>t</sub> = the first valid market closing price (from Compustat) of an IPO within a $[-3, +60]$ day window around the `Issue_Date` t (from SDC), prioritizing the exact issue date, followed by the closest subsequent day, and lastly the closest preceding day.
      - P<sub>offer</sub> = `Offer_Price_USD` of the IPO (from SDC)
- **Input**: `Input/Compustat/global_security_daily_price_2014_2024.csv`, `Stata/IPO_2015_2019_with_market_return_and_market_volatility_0621.dta`
- **Output**: `Stata/IPO_2015_2019_with_ipo_underpricing_0621.dta`
- **Match result**: A total of 2344 rows were exported. This includes 2082 successful matches, along with 262 unmapped rows. Unmapped reasons:
  - ISIN and SEDOL not found in security database: 219
  - No trading records within date range (-3, +60): 43
#### 3-3. Divide by DataStream listed equities (`3-3_DataStream_listed_equity.py`)
- **Objective**: 
  - Calculate `IPO_Activities` as the natural log of `IPO_count` (from SDC) divided by DataStream listed equities (CSV).
  - Calculate `AFOL` as `Total_AFOL` divided by DataStream listed equities (CSV).
- **Input**: `Stata/IPO_2015_2019_with_ipo_underpricing_0621.dta`, `Input/Worldscope_fundamental_variables.csv`
- **Output**: `Stata/IPO_2015_2019_divided_by_DataStream_listed_equities_0621.dta`
- **Match result**: A total of 2,344 rows were exported. This includes 1,926 successful matches, along with 418 unmapped rows.
#### 4. Column Filtering (`filter.py`)
- **Objective**: drop unnecessary variables for model 1 and calculate samples dropped for each stage.
- **Input**: `Stata/IPO_2015_2019_divided_by_DataStream_listed_equities_0621.dta`
- **Output**: `Stata/IPO_2015_2019_filtered_0621.dta`
- **Missing value proportions per column**:
sedol                        0/2344
isin                         0/2344
dscd                         0/2344
year                         0/2344
country                      0/2344
country_code2                0/2344
sic2digit                  418/2344
Underpricing               262/2344
Post                         0/2344
lease_intensity_pre        418/2344
high_lease                 418/2344
SME_IFRS_adoption            0/2344
Ln_Age                     809/2344
BIGN                       418/2344
Ln_Sales                   617/2344
Capex_TA                  1281/2344
RD_TA                      617/2344
ROA_EBITDA                 706/2344
LEV                        617/2344
INST                       114/2344
Relative_Offer_Size        617/2344
VC_backed                   10/2344
Firm_Commitment              0/2344
Underwriter_Reputation       0/2344
Bookbuilt                    0/2344
Market_Return                0/2344
Market_Volatility            0/2344
IPO_Activities               0/2344
Price_Stabilization          0/2344
Economic_Freedom             4/2344
CAP_Ratio                    7/2344
Ln_GDP_per_capita_US         4/2344
GDP_per_capita_growth        4/2344
AFOL                         0/2344
---
#### Country and Stock Index Reference Table
Worldscope(DataStream) Variable Definitions (2023): https://drive.google.com/file/d/1ZE9ln7Hpz22WhWdok19RgPY0qKA8y-DU/view?usp=drive_link
| Country | Stock Index |
| :--- | :--- |
| Argentina | Indice MERVAL Argentino |
| Australia | All Australia Ordinaries |
| Austria | ATX Austrian Traded Index |
| Belgium | BEL 20 Index |
| Brazil | BOVESPA |
| Canada | S&P/TSX Composite Index |
| Denmark | Copenhagen KFX Index |
| Finland | All Share Price Index |
| France | SBF 250 Index |
| Germany | HDAX |
| Greece | Athens Composite Index |
| Hong Kong | Hang Seng Index |
| Hungary | BUX Index |
| Indonesia | Jakarta Composite Price Index |
| Ireland | SEQ-Overall (Price) |
| Italy | FTSE Italia All Share |
| Japan | Nikkei 225 Index |
| Korea | Korea Composite Index |
| Malaysia | KLSE Composite Index |
| Mexico | IPC Index |
| Netherlands | AEX Index |
| New Zealand | NZ50 (GRS) |
| Norway | Oslo Bors Benchmark Index |
| Pakistan | Pakistan |
| Peru | IGBVL Index |
| Philippines | Philippines Composite Index |
| Poland | Warsaw WIG Index |
| Portugal | PSI General |
| Singapore | Straits Times Index |
| South Africa | Africa All Shares Index |
| Spain | Madrid Stock Exchange |
| Sweden | OMX Stock Index |
| Switzerland | Swiss Market Index |
| Taiwan | Taiwan Stock Exchange Weighted Index |
| Thailand | Bangkok Stock Exchange SET Index |
| Turkey | ISE National 100 |
| United Kingdom | FT All Share |
| United States | S&P 500 |
| Venezuela | IBC General |
