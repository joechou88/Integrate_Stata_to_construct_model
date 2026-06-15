import pandas as pd
import config

print(f"Loading datasets:\n  - {config.WORLDSCOPE_EQUITY_COUNTS_OUTPUT}")
stata_df = pd.read_stata(config.WORLDSCOPE_EQUITY_COUNTS_OUTPUT)

ordered_columns = [
    "Underpricing", 
    "Post", 
    "High_Lease", 
    "PostxHigh_Lease", 
    "Ln_Age", 
    "BIGN", 
    "MB", 
    "Ln_Sales", 
    "Capex_Sales", 
    "RD_Sales", 
    "ROA_EBITDA", 
    "LEV", 
    "ABS_ABACC", 
    "INST", 
    "Relative_offer_size", 
    "VC_backed", 
    "Firm_Commitment", 
    "Underwriter_Reputation", 
    "Bookbuilt", 
    "Equity_Carve_out", 
    "Market_Return", 
    "Market_Volatility", 
    "IPO_Activities", 
    "Price_Stabilization", 
    "Economic_Freedom", 
    "Country_Q", 
    "CAP_Ratio", 
    "GDP_per_capita_US", 
    "GDP_per_capita_growth", 
    "AFOL"
]

# Ensure we only try to keep columns that actually exist in the dataframe to prevent KeyErrors.
# If your column names differ slightly (e.g., 'BigN' instead of 'BIGN'), adjust the list above.
missing_cols = [col for col in ordered_columns if col not in stata_df.columns]
if missing_cols:
    print(f"[Warning] The following columns were not found in the dataset and will be skipped: {missing_cols}")

valid_columns = [col for col in ordered_columns if col in stata_df.columns]
merged_df = stata_df[valid_columns].copy()

output_path = config.FILTERED_OUTPUT
merged_df.to_stata(output_path, write_index=False)
print(f"Exported to: {output_path}")
