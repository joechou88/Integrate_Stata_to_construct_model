import os

# Folder name
INPUT_DIR = "Input"
LEASE_DIR = "Lease"
AFOL_DIR = "AFOL"
INST_DIR = "INST"
COMPUSTAT_DIR = "Compustat"
STATA_DIR = "Stata"

# File name
LEASE_NPV_INPUT_2015_2024 = os.path.join(STATA_DIR, "Financial_npv_lease20152024_0620.dta")
suffix = ""
if "_0620" in LEASE_NPV_INPUT_2015_2024:
    suffix = "_0620"
elif "_0621" in LEASE_NPV_INPUT_2015_2024:
    suffix = "_0621"
CONTROLS_INPUT_1996_2019 = os.path.join(INPUT_DIR, "calc_controls_1996_2019.sas7bdat")
NPV_LEASE_2000_2019 = os.path.join(INPUT_DIR, LEASE_DIR, "npv_lease_2000_2019_202606_sic.sas7bdat")
ROU_2015_2024 = os.path.join(INPUT_DIR, LEASE_DIR, "ROU_2015_2024.sas7bdat")
SDC_INPUT = os.path.join(INPUT_DIR, "Calculated_All_countries_SDC_2015-2024.xlsx")
COUNTRY_CODE_INPUT = os.path.join(INPUT_DIR, "country_code.xlsx")
COUNTRY_LEVEL_CONTROLS_INPUT = os.path.join(INPUT_DIR, "country_controls.xlsx")
IBES_NON_US_INPUT = os.path.join(INPUT_DIR, AFOL_DIR, "ibes_non_us_1983_2025.sas7bdat")
IBES_US_INPUT = os.path.join(INPUT_DIR, AFOL_DIR, "ibes_us_1983_2025.sas7bdat")
IBES_INT_INPUT = os.path.join(INPUT_DIR, AFOL_DIR, "ibes_int_1983_2025.sas7bdat")
INST_INPUT = os.path.join(INPUT_DIR, INST_DIR, "inst_1997_2025.sas7bdat")
SME_INPUT = os.path.join(INPUT_DIR, "SME_IFRS_adoption.xlsx")
MARKET_PRICE_INPUT = os.path.join(INPUT_DIR, COMPUSTAT_DIR, "global_market_price_2014_2024_with_country_code.csv")
SECURITY_PRICE_INPUT = os.path.join(INPUT_DIR, COMPUSTAT_DIR, "global_security_daily_price_2014_2024.csv")
WORLDSCOPE_FUNDAMENTALS_INPUT = os.path.join(INPUT_DIR, "Worldscope_fundamental_variables.csv")

LEASE_NPV_OUTPUT_2014_2024 = os.path.join(STATA_DIR, f"Financial_npv_lease20142024{suffix}.dta")
LAG_OUTPUT = os.path.join(STATA_DIR, f"Financial_npv_lease20142024_lag_variables{suffix}.dta")
NPV_LEASE_OUTPUT = os.path.join(STATA_DIR, f"Financial_npv_lease20142024_lag_variables{suffix}.dta")
SDC_OUTPUT = os.path.join(STATA_DIR, f"IPO_2015_2024{suffix}.dta")
COUNTRY_LEVEL_CONTROLS_OUTPUT = os.path.join(STATA_DIR, f"IPO_2015_2024_with_country_level_controls{suffix}.dta")
AFOL_OUTPUT = os.path.join(STATA_DIR, f"IPO_2015_2024_with_AFOL{suffix}.dta")
INST_OUTPUT = os.path.join(STATA_DIR, f"IPO_2015_2024_with_INST{suffix}.dta")
SME_OUTPUT = os.path.join(STATA_DIR, f"IPO_2015_2024_with_SME_IFRS_adoption{suffix}.dta")
DERIVE_COLUMNS_OUTPUT = os.path.join(STATA_DIR, f"IPO_2015_2024_derive_columns{suffix}.dta")
RELATIVE_OFFER_SIZE_OUTPUT = os.path.join(STATA_DIR, f"IPO_2015_2024_with_relative_offer_size{suffix}.dta")
MARKET_PRICE_OUTPUT = os.path.join(STATA_DIR, f"IPO_2015_2024_with_market_return_and_market_volatility{suffix}.dta")
SECURITY_PRICE_OUTPUT = os.path.join(STATA_DIR, f"IPO_2015_2024_with_ipo_underpricing{suffix}.dta")
WORLDSCOPE_EQUITY_COUNTS_OUTPUT = os.path.join(STATA_DIR, f"IPO_2015_2024_with_ipo_activities{suffix}.dta")
FILTERED_OUTPUT = os.path.join(STATA_DIR, f"IPO_2015_2024_filtered{suffix}.dta")
