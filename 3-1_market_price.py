import pandas as pd
import numpy as np
import config

print(f"Loading datasets:\n  - {config.MARKET_PRICE_INPUT}\n  - {config.DERIVE_COLUMNS_OUTPUT}")
market_df = pd.read_csv(config.MARKET_PRICE_INPUT)
stata_df = pd.read_stata(config.DERIVE_COLUMNS_OUTPUT)

market_df['_merge_cc'] = market_df['Country_code'].astype(str).str.strip().str.upper()
market_df['datadate'] = pd.to_datetime(market_df['datadate'], errors='coerce').dt.tz_localize(None)
market_df['prccd'] = pd.to_numeric(market_df['prccd'], errors='coerce')
market_df = market_df.dropna(subset=['_merge_cc', 'datadate', 'prccd']).sort_values(['_merge_cc', 'datadate'])

print("Calculating Market_Return and Market_Volatility...")
market_df['daily_return'] = market_df.groupby('_merge_cc')['prccd'].pct_change()
market_df['Market_Volatility'] = market_df.groupby('_merge_cc')['daily_return'].transform(lambda x: x.rolling(21).std())
market_df['Market_Return'] = np.log(market_df['prccd'] / market_df.groupby('_merge_cc')['prccd'].shift(90))
market_df = market_df[['_merge_cc', 'datadate', 'Market_Return', 'Market_Volatility']]
market_df = market_df.drop_duplicates(subset=['_merge_cc', 'datadate'], keep='last')
market_df = market_df.sort_values('datadate')

stata_df = stata_df.copy()
stata_df['_orig_index'] = stata_df.index
stata_df['_merge_cc'] = stata_df['country_code2'].astype(str).str.strip().str.upper()
stata_df['temp_bdate'] = pd.to_datetime(stata_df['Issue_Date'], errors='coerce').dt.tz_localize(None)
valid_mask = stata_df['temp_bdate'].notna()
stata_valid = stata_df[valid_mask].copy()
stata_invalid = stata_df[~valid_mask].copy()
stata_valid['merge_date'] = stata_valid['temp_bdate'] - pd.Timedelta(days=1)
stata_valid = stata_valid.sort_values('merge_date')

print("Merging datasets...")
merged_valid = pd.merge_asof(
    stata_valid,
    market_df,
    left_on='merge_date',
    right_on='datadate',
    by='_merge_cc',
    direction='backward'
)

merged_df = pd.concat([merged_valid, stata_invalid], ignore_index=True)
merged_df = merged_df.sort_values('_orig_index')
merged_df = merged_df.drop(columns=['_orig_index', '_merge_cc', 'temp_bdate', 'merge_date', 'datadate'], errors='ignore')

output_path = config.MARKET_PRICE_OUTPUT
merged_df.to_stata(output_path, write_index=False)
print(f"\n[OK] Done! Successfully wrote {len(merged_df)} rows to {output_path}")
