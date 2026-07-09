import os

START_YEAR = 2015
END_YEAR = 2024

# Folder name
INPUT_DIR = "Input"
LEASE_DIR = "Lease"
AFOL_DIR = "AFOL"
INST_DIR = "INST"
COMPUSTAT_DIR = "Compustat"
STATA_DIR = "Stata"

# File name
LEASE_NPV_INPUT_2015_2024 = os.path.join(STATA_DIR, "Financial_npv_lease20152024_0621.dta")
suffix = ""
if "_0620" in LEASE_NPV_INPUT_2015_2024:
    suffix = "_0620"
elif "_0621" in LEASE_NPV_INPUT_2015_2024:
    suffix = "_0621"
COUNTRY_CODE_WITH_CURD = os.path.join(INPUT_DIR, "country_code_with_curd.xlsx")
EXCHANGE_RATE_2015_2024 = os.path.join(INPUT_DIR, COMPUSTAT_DIR, "global_exchange_rate_2015_2024.csv")
CONTROLS_INPUT_1996_2019 = os.path.join(INPUT_DIR, "calc_controls_1996_2019.sas7bdat")
NPV_LEASE_2000_2019 = os.path.join(INPUT_DIR, LEASE_DIR, "npv_lease_2000_2019_202606_sic.sas7bdat")
ROU_2015_2024 = os.path.join(INPUT_DIR, LEASE_DIR, "ROU_2015_2024.sas7bdat")
SDC_INPUT = os.path.join(INPUT_DIR, f"Calculated_All_countries_SDC_{START_YEAR}-{END_YEAR}.xlsx")
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
ORIGIN_LEASE_2000_2019 = os.path.join(INPUT_DIR, LEASE_DIR, "npv_lease_43country_2000_2019.csv")

LEASE_NPV_OUTPUT_2014_2024 = os.path.join(STATA_DIR, f"Financial_npv_lease20142024{suffix}.dta")
LAG_OUTPUT = os.path.join(STATA_DIR, f"Financial_npv_lease20142024_lag_variables{suffix}.dta")
NPV_LEASE_OUTPUT = os.path.join(STATA_DIR, f"Financial_npv_lease20142024_lag_variables{suffix}.dta")
SDC_OUTPUT = os.path.join(STATA_DIR, f"IPO_{START_YEAR}_{END_YEAR}{suffix}.dta")
OFFER_PRICE_OUTPUT = os.path.join(STATA_DIR, f"IPO_{START_YEAR}_{END_YEAR}_with_updated_offer_price{suffix}.dta")
COUNTRY_LEVEL_CONTROLS_OUTPUT = os.path.join(STATA_DIR, f"IPO_{START_YEAR}_{END_YEAR}_with_country_level_controls{suffix}.dta")
AFOL_OUTPUT = os.path.join(STATA_DIR, f"IPO_{START_YEAR}_{END_YEAR}_with_AFOL{suffix}.dta")
INST_OUTPUT = os.path.join(STATA_DIR, f"IPO_{START_YEAR}_{END_YEAR}_with_INST{suffix}.dta")
SME_OUTPUT = os.path.join(STATA_DIR, f"IPO_{START_YEAR}_{END_YEAR}_with_SME_IFRS_adoption{suffix}.dta")
DERIVE_COLUMNS_OUTPUT = os.path.join(STATA_DIR, f"IPO_{START_YEAR}_{END_YEAR}_derive_columns{suffix}.dta")
RELATIVE_OFFER_SIZE_OUTPUT = os.path.join(STATA_DIR, f"IPO_{START_YEAR}_{END_YEAR}_with_relative_offer_size{suffix}.dta")
MARKET_PRICE_OUTPUT = os.path.join(STATA_DIR, f"IPO_{START_YEAR}_{END_YEAR}_with_market_return_and_market_volatility{suffix}.dta")
SECURITY_PRICE_OUTPUT = os.path.join(STATA_DIR, f"IPO_{START_YEAR}_{END_YEAR}_with_ipo_underpricing{suffix}.dta")
WORLDSCOPE_EQUITY_COUNTS_OUTPUT = os.path.join(STATA_DIR, f"IPO_{START_YEAR}_{END_YEAR}_divided_by_DataStream_listed_equities{suffix}.dta")
FILTERED_OUTPUT = os.path.join(STATA_DIR, f"IPO_{START_YEAR}_{END_YEAR}_filtered{suffix}.dta")
MARK_OUTPUT = os.path.join(STATA_DIR, f"IPO_{START_YEAR}_{END_YEAR}_marked_lease_intensity_pre{suffix}.dta")
