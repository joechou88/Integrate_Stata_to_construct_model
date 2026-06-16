import pandas as pd
import config

print(f"Loading datasets:\n- {config.DERIVE_COLUMNS_OUTPUT}")
stata_df = pd.read_stata(config.DERIVE_COLUMNS_OUTPUT).copy()

stata_df["company_id"] = (
    stata_df["sedol"]
    .combine_first(stata_df["isin"])
    .combine_first(stata_df["dscd"])
)
stata_df = stata_df.sort_values(by=["company_id", "year"])
previous_year_total_assets = stata_df.groupby("company_id")["total_assets"].shift(1)
stata_df["Relative_Offer_Size"] = stata_df["Relative_Offer_Size"] / previous_year_total_assets

output_path = config.RELATIVE_OFFER_SIZE_OUTPUT
stata_df.to_stata(output_path, write_index=False)
print(f"Exported to: {output_path}")
