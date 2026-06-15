import pandas as pd
import config

price_df = pd.read_csv(config.SECURITY_PRICE_INPUT)

arg_df = price_df[price_df['fic'] == 'ARG'].copy()

output_path = "Argentina_global_security_daily_price_2014_2024.csv"
arg_df.to_csv(output_path, index=False)
print(f"Exported to: {output_path}")