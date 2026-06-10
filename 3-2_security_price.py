import pandas as pd
import config

print(f"Loading datasets:\n  - {config.MARKET_PRICE_OUTPUT}\n  - {config.SECURITY_PRICE_INPUT}")
stata_df = pd.read_stata(config.MARKET_PRICE_OUTPUT)
security_df = pd.read_csv(config.SECURITY_PRICE_INPUT, usecols=['isin', 'datadate', 'prccd'])

stata_df['Issue_Date'] = pd.to_datetime(stata_df['Issue_Date'])
security_df['datadate'] = pd.to_datetime(security_df['datadate'])
valid_isins = stata_df['isin'].dropna().unique()
valid_dates = stata_df['Issue_Date'].dropna().unique()
price_subset = security_df[
    (security_df['isin'].isin(valid_isins)) & 
    (security_df['datadate'].isin(valid_dates))
].copy()
price_subset = price_subset.drop_duplicates(subset=['isin', 'datadate'], keep='last')

print("\nMerging data to find first-day closing price...")
merged_df = pd.merge(
    stata_df, 
    price_subset, 
    left_on=['isin', 'Issue_Date'], 
    right_on=['isin', 'datadate'], 
    how='left'
)

print("Calculating Underpricing...")
merged_df['Underpricing'] = (merged_df['prccd'] - merged_df['Offer_Price_USD']) / merged_df['Offer_Price_USD']

merged_df = merged_df.drop(columns=['datadate', 'prccd'], errors='ignore')

output_path = config.SECURITY_PRICE_OUTPUT
merged_df.to_stata(output_path, write_index=False)
print(f"\n[OK] Done! Successfully wrote {len(merged_df)} rows to {output_path}")
