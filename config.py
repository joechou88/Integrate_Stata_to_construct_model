import os

# Folder name
EXCEL_DIR = "Excel_to_be_merged"
STATA_DIR = "Stata"

# File name
SDC_INPUT = os.path.join(EXCEL_DIR, "Calculated_All_countries_SDC_2015-2024.xlsx")
COUNTRY_LEVEL_CONTROLS_INPUT = os.path.join(EXCEL_DIR, "country_control_all.20200524_final.xlsx")
STATA_INPUT = os.path.join(STATA_DIR, "Financial_npv_lease20152024.dta")
STATA_SDC_OUTPUT = os.path.join(STATA_DIR, "Financial_npv_lease20152024_SDC.dta")
STATA_COUNTRY_LEVEL_CONTROLS_OUTPUT = os.path.join(STATA_DIR, "Financial_npv_lease20152024_add_country_level_controls.dta")
