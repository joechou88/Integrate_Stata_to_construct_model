import pandas as pd
import config

print(f"Loading datasets:\n  - {'0-3_missing_lease.xlsx'}\n  - {config.SDC_OUTPUT}")
excel_df = pd.read_excel("0-3_missing_lease.xlsx", sheet_name=None)
combined_excel_df = pd.concat(excel_df.values())
stata_df = pd.read_stata(config.SDC_OUTPUT)

stata_missing_lease_df = stata_df[stata_df['Lease_Intensity'].isna()]
stata_missing_dscd = set(stata_missing_lease_df['dscd'].unique())

set_excel_dscd = set(combined_excel_df['dscd'].unique())
present_in_excel = stata_missing_dscd.intersection(set_excel_dscd)
missing_from_excel = stata_missing_dscd.difference(set_excel_dscd)

print(f"Total unique dscd with missing Lease_Intensity in Stata: {len(stata_missing_dscd)}")
print(f"Count of those dscd present in Excel: {len(present_in_excel)}")
print(f"Count of those dscd missing from Excel: {len(missing_from_excel)}")

with pd.ExcelWriter("check_IPO_missing_lease.xlsx") as writer:
    for sheet_name, sheet_df in excel_df.items():
        filtered_df = sheet_df[sheet_df['dscd'].isin(present_in_excel)]
        filtered_df.to_excel(writer, sheet_name=sheet_name, index=False)
print("Successfully saved present dscd to 'check_IPO_missing_lease.xlsx'")