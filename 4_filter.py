import pandas as pd
import config

print(f"Loading datasets:\n  - {config.WORLDSCOPE_EQUITY_COUNTS_OUTPUT}")
stata_df = pd.read_stata(config.WORLDSCOPE_EQUITY_COUNTS_OUTPUT)

stata_df.rename(columns={'bign': 'BIGN', 'mb': 'MB', 'ln_sales': 'Ln_Sales', 'capex_sales': 'Capex_Sales', 'rd_sales': 'RD_Sales', 'roa_ebitda': 'ROA_EBITDA', 'lev': 'LEV', 'abs_abacc': 'ABS_ABACC', 'tobin': 'Tobin_Q'}, inplace=True)

ordered_columns = [
    "Underpricing",
    "Post",
    # "Lease_Intensity", 
    # "PostxLease_Intensity",
    "SME_IFRS_adoption",
    "Ln_Age",
    "BIGN",
    "Ln_Sales",
    "Capex_Sales",
    "RD_Sales",
    "ROA_EBITDA",
    "LEV",
    "INST",
    "Relative_Offer_Size",
    "VC_backed",
    "Firm_Commitment",
    "Underwriter_Reputation",
    "Bookbuilt",
    "Market_Return",
    "Market_Volatility",
    "IPO_Activities",
    "Price_Stabilization",
    "Economic_Freedom",
    "CAP_Ratio",
    "GDP_per_capita_US",
    "GDP_per_capita_growth",
    "AFOL"
]

missing_cols = [col for col in ordered_columns if col not in stata_df.columns]
if missing_cols:
    print(f"[Warning] The following columns were not found in the dataset and will be skipped: {missing_cols}")

valid_columns = [col for col in ordered_columns if col in stata_df.columns]
merged_df = stata_df[valid_columns].copy()

total_rows = len(merged_df)
missing_value_proportions = merged_df.isnull().sum().astype(str) + "/" + str(total_rows)
print("Missing value proportions per column:\n", missing_value_proportions)
merged_df = merged_df.dropna()
remaining_sample_count = len(merged_df)
print(f"Remaining samples after dropping rows with missing values: {remaining_sample_count}")

output_path = config.FILTERED_OUTPUT
merged_df.to_stata(output_path, write_index=False)
print(f"Exported to: {output_path}")
