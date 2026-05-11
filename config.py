import os

# Folder name
STATA_DIR = "Stata"

# File name
SDC_INPUT = "Calculated_All_countries_SDC_2015-2024.xlsx"
STATA_INPUT = os.path.join(STATA_DIR, "Financial_npv_lease20152024.dta")
STATA_OUTPUT = os.path.join(STATA_DIR, "Financial_npv_lease20152024_20260511.dta")
