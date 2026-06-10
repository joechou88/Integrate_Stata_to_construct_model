import os

# Folder name
INPUT_DIR = "Input"
AFOL_DIR = "AFOL"
INST_DIR = "INST"
COMPUSTAT_DIR = "Compustat"
STATA_DIR = "Stata"

# File name
SDC_INPUT = os.path.join(INPUT_DIR, "Calculated_All_countries_SDC_2015-2024.xlsx")
COUNTRY_LEVEL_CONTROLS_INPUT = os.path.join(INPUT_DIR, "country_controls.xlsx")
WORLDSCOPE_FUNDAMENTALS_INPUT = os.path.join(STATA_DIR, "Financial_npv_lease20152024.dta")
IBES_NON_US_INPUT = os.path.join(INPUT_DIR, AFOL_DIR, "ibes_non_us_1983_2025.sas7bdat")
IBES_US_INPUT = os.path.join(INPUT_DIR, AFOL_DIR, "ibes_us_1983_2025.sas7bdat")
IBES_INT_INPUT = os.path.join(INPUT_DIR, AFOL_DIR, "ibes_int_1983_2025.sas7bdat")
INST_INPUT = os.path.join(INPUT_DIR, INST_DIR, "inst_1997_2025.sas7bdat")
MARKET_PRICE_INPUT = os.path.join(INPUT_DIR, COMPUSTAT_DIR, "global_market_price_2014_2024_with_country_code.csv")
SECURITY_PRICE_INPUT = os.path.join(INPUT_DIR, COMPUSTAT_DIR, "global_security_daily_price_2014_2024.csv")

SDC_OUTPUT = os.path.join(STATA_DIR, "IPO_2015_2024.dta")
COUNTRY_LEVEL_CONTROLS_OUTPUT = os.path.join(STATA_DIR, "IPO_2015_2024_with_country_level_controls.dta")
AFOL_OUTPUT = os.path.join(STATA_DIR, "IPO_2015_2024_with_AFOL.dta")
INST_OUTPUT = os.path.join(STATA_DIR, "IPO_2015_2024_with_INST.dta")
DERIVE_COLUMNS_OUTPUT = os.path.join(STATA_DIR, "IPO_2015_2024_derive_columns.dta")
MARKET_PRICE_OUTPUT = os.path.join(STATA_DIR, "IPO_2015_2024_with_market_return_and_market_volatility.dta")
SECURITY_PRICE_OUTPUT = os.path.join(STATA_DIR, "IPO_2015_2024_with_ipo_underpricing.dta")
FILTERED_OUTPUT = f"IPO_2015_2024_filtered.xlsx"
STATA_Model1_OUTPUT = os.path.join(STATA_DIR, "IPO_2015_2024_model_1.dta")
STATA_Model2_OUTPUT = os.path.join(STATA_DIR, "IPO_2015_2024_model_2.dta")
STATA_Model3_OUTPUT = os.path.join(STATA_DIR, "IPO_2015_2024_model_3.dta")
