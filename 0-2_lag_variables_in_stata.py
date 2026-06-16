import pandas as pd
import config

print(f"Loading datasets:\n  - {config.OPERATING_LEASE_NPV_INPUT}")
stata_df = pd.read_stata(config.OPERATING_LEASE_NPV_INPUT).copy()

stata_df["company_id"] = (
    stata_df["sedol"]
    .combine_first(stata_df["isin"])
    .combine_first(stata_df["dscd"])
)
valid_rows = stata_df["company_id"].notna().sum()
stata_df = stata_df.sort_values(by=["company_id", "year"])
columns_to_lag = ["ln_sales", "capex_sales", "rd_sales", "roa_ebitda", "lev", "abs_abacc"]
successful_updates = {column: 0 for column in columns_to_lag}

for column in columns_to_lag:
    lagged_values = stata_df.groupby("company_id")[column].shift(1)
    year_difference = stata_df.groupby("company_id")["year"].diff()
    valid_lag_mask = (year_difference == 1) & lagged_values.notna()
    successful_updates[column] = valid_lag_mask.sum()
    stata_df[column] = stata_df[column].mask(year_difference == 1, lagged_values)

stata_df = stata_df.drop(columns=["company_id"])

print(f"Original {len(stata_df)} rows. Detailed updates per column:")
for column in columns_to_lag:
    print(f"  - {column:<12}: {successful_updates[column]}/{valid_rows} updated successfully")

output_path = config.LAG_OUTPUT
stata_df.to_stata(output_path, write_index=False)
print(f"Exported to: {output_path}")
