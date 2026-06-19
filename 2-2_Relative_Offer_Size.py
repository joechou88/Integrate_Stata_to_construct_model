import pandas as pd
import config

print(f"Loading datasets:\n- {config.DERIVE_COLUMNS_OUTPUT}")
stata_df = pd.read_stata(config.DERIVE_COLUMNS_OUTPUT).copy()

stata_df["Relative_Offer_Size"] = stata_df["Relative_Offer_Size"] / stata_df["total_assets_lag"]

output_path = config.RELATIVE_OFFER_SIZE_OUTPUT
stata_df.to_stata(output_path, write_index=False)
print(f"Exported to: {output_path}")
