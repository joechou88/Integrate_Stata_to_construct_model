import pandas as pd
import numpy as np
import config

print(f"Loading datasets:\n  - {config.MARKET_PRICE_OUTPUT}\n  - {config.SECURITY_PRICE_INPUT}")
stata_df = pd.read_stata(config.MARKET_PRICE_OUTPUT)
security_df = pd.read_csv(config.SECURITY_PRICE_INPUT, usecols=['isin', 'datadate', 'prccd'])

stata_df['Issue_Date'] = pd.to_datetime(stata_df['Issue_Date'])
security_df['datadate'] = pd.to_datetime(security_df['datadate'])
valid_isins = stata_df['isin'].dropna().unique()
valid_dates = stata_df['Issue_Date'].dropna().unique()

price_subset = security_df[security_df['isin'].isin(valid_isins)].dropna(subset=['prccd']).copy()
price_subset = price_subset.drop_duplicates(subset=['isin', 'datadate'], keep='last')
print("\nMerging data to find first valid closing price within [-3, +60] days...")
stata_df['_row_id'] = np.arange(len(stata_df))
temp_merge = pd.merge(
    stata_df[['_row_id', 'isin', 'Issue_Date']], 
    price_subset, 
    on='isin', 
    how='left'
)
temp_merge['days_diff'] = (temp_merge['datadate'] - temp_merge['Issue_Date']).dt.days
valid_prices = temp_merge[temp_merge['days_diff'].between(-3, 60)].copy()
valid_prices['sort_key'] = np.where(
    valid_prices['days_diff'] >= 0, 
    valid_prices['days_diff'], 
    100 - valid_prices['days_diff']
)
best_prices = valid_prices.sort_values(['_row_id', 'sort_key']).drop_duplicates(subset=['_row_id'], keep='first')

print("\nMerging data to find first-day closing price...")
merged_df = pd.merge(
    stata_df,
    best_prices[['_row_id', 'datadate', 'prccd']],
    on='_row_id',
    how='left'
)

print("Calculating Underpricing...")
merged_df['Underpricing'] = (merged_df['prccd'] - merged_df['Offer_Price_USD']) / merged_df['Offer_Price_USD']

missing_count = merged_df['Underpricing'].isna().sum()
total_count = len(merged_df)
print(f"Number of firms missing Underpricing: {missing_count} / {total_count}")

merged_df = merged_df.drop(columns=['_row_id', 'datadate', 'prccd'], errors='ignore')
merged_df['Issue_Date'] = merged_df['Issue_Date'].dt.strftime('%Y-%m-%d')

output_path = config.SECURITY_PRICE_OUTPUT
merged_df.to_stata(output_path, write_index=False)
print(f"\n[OK] Done! Successfully wrote {len(merged_df)} rows to {output_path}")
