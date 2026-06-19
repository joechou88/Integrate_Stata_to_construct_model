import pandas as pd
import config

print(f"Loading datasets:\n  - {config.LEASE_NPV_OUTPUT_2014_2024}")
stata_df = pd.read_stata(config.LEASE_NPV_OUTPUT_2014_2024).copy()

stata_df["company_id"] = (
    stata_df["sedol"]
    .combine_first(stata_df["isin"])
    .combine_first(stata_df["dscd"])
)
columns_to_lag = ["ln_sales", "capex_sales", "rd_sales", "roa_ebitda", "lev", "abs_abacc", "total_assets"]

lag_df = stata_df[["company_id", "year"] + columns_to_lag].drop_duplicates(subset=["company_id", "year"])
lag_df["year"] = lag_df["year"] + 1
rename_dict = {col: f"{col}_lag" for col in columns_to_lag}
lag_df = lag_df.rename(columns=rename_dict)
stata_df = stata_df.merge(lag_df, on=["company_id", "year"], how="left")
stata_df = stata_df.drop(columns=["company_id"])

valid_rows = len(stata_df)
print(f"Original {valid_rows} rows. Detailed updates per column:")
for column in columns_to_lag:
    new_col_name = f"{column}_lag"
    success_count = stata_df[new_col_name].notna().sum()
    print(f"  - {new_col_name:<18}: {success_count}/{valid_rows} updated successfully")

output_path = config.LAG_OUTPUT
stata_df.to_stata(output_path, write_index=False)
print(f"Exported to: {output_path}")
