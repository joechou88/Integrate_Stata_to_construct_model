import pandas as pd
import config

price_df = pd.read_csv(config.SECURITY_PRICE_INPUT)

price_df = price_df[['sedol', 'prccd']]
sedol_to_price = price_df.groupby('sedol')['prccd'].nunique().reset_index()
duplicate_prices_df = sedol_to_price[sedol_to_price['prccd'] > 1].copy()

output_path = "sedols_with_duplicate_prices.csv"
duplicate_prices_df.to_csv(output_path, index=False)
print(f"Exported to: {output_path}")