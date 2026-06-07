import os

# Folder name
INPUT_DIR = "Input"
STATA_DIR = "Stata"

# File name
SDC_INPUT = os.path.join(INPUT_DIR, "Calculated_All_countries_SDC_2015-2024.xlsx")
COUNTRY_LEVEL_CONTROLS_INPUT = os.path.join(INPUT_DIR, "country_controls.xlsx")
STATA_INPUT = os.path.join(STATA_DIR, "Financial_npv_lease20152024.dta")
STATA_SDC_OUTPUT = os.path.join(STATA_DIR, "IPO_2015_2024.dta")
STATA_COUNTRY_LEVEL_CONTROLS_OUTPUT = os.path.join(STATA_DIR, "IPO_2015_2024_with_country_level_controls.dta")
IBES_NON_US_INPUT = os.path.join(INPUT_DIR, "ibes_non_us_1983_2025.sas7bdat")
IBES_US_INPUT = os.path.join(INPUT_DIR, "ibes_us_1983_2025.sas7bdat")
IBES_INT_INPUT = os.path.join(INPUT_DIR, "ibes_int_1983_2025.sas7bdat")
STATA_DERIVE_COLUMNS_OUTPUT = os.path.join(STATA_DIR, "IPO_2015_2024_derive_columns.dta")

STATA_AFOL_OUTPUT = os.path.join(STATA_DIR, "IPO_2015_2024_with_AFOL.dta")
STATA_Model1_OUTPUT = os.path.join(STATA_DIR, "IPO_2015_2024_model_1.dta")
STATA_Model2_OUTPUT = os.path.join(STATA_DIR, "IPO_2015_2024_model_2.dta")
STATA_Model3_OUTPUT = os.path.join(STATA_DIR, "IPO_2015_2024_model_3.dta")
