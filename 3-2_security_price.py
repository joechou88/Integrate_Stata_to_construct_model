import pandas as pd
import numpy as np
import config

print(f"Loading datasets:\n  - {config.MARKET_PRICE_OUTPUT}\n  - {config.SECURITY_PRICE_INPUT}")
stata_df = pd.read_stata(config.MARKET_PRICE_OUTPUT)
security_df = pd.read_csv(
    config.SECURITY_PRICE_INPUT, 
    usecols=['isin', 'sedol', 'datadate', 'prccd']
).rename(columns={'datadate': 'price_date', 'prccd': 'closing_price'})

stata_df['Issue_Date'] = pd.to_datetime(stata_df['Issue_Date'])
security_df['price_date'] = pd.to_datetime(security_df['price_date'])

security_df = security_df.dropna(subset=['closing_price'])
security_df = security_df.drop_duplicates(subset=['isin', 'sedol', 'price_date'], keep='last')

stata_df = stata_df.reset_index(names='original_row_index')

# ==========================================
# Phase 1: Merge by ISIN
# ==========================================
merged_df = pd.merge(
    stata_df[['original_row_index', 'isin', 'Issue_Date']], 
    security_df, 
    on='isin', 
    how='left'
)

merged_df['days_difference'] = (merged_df['price_date'] - merged_df['Issue_Date']).dt.days
valid_prices_window = merged_df[merged_df['days_difference'].between(-3, 60)].copy()
valid_prices_window['sorting_priority'] = np.where(
    valid_prices_window['days_difference'] >= 0, 
    valid_prices_window['days_difference'], 
    100 - valid_prices_window['days_difference']
)

best_matching_prices = valid_prices_window.sort_values(
    ['original_row_index', 'sorting_priority']
).drop_duplicates(subset=['original_row_index'], keep='first')

merged_df = pd.merge(
    stata_df,
    best_matching_prices[['original_row_index', 'closing_price']],
    on='original_row_index',
    how='left'
)

merged_df['Underpricing'] = (merged_df['closing_price'] - merged_df['Offer_Price_USD']) / merged_df['Offer_Price_USD']

# ==========================================
# Phase 2: Merge by SEDOL
# ==========================================
mapped_df = merged_df[~merged_df['Underpricing'].isna()].copy()
unmapped_df = merged_df[merged_df['Underpricing'].isna()].copy()
unmapped_df = unmapped_df.drop(columns=['closing_price', 'Underpricing'])

merged_df_by_sedol = pd.merge(
    unmapped_df[['original_row_index', 'sedol', 'Issue_Date']], 
    security_df.dropna(subset=['sedol']), 
    on='sedol', 
    how='left'
)

merged_df_by_sedol['days_difference'] = (merged_df_by_sedol['price_date'] - merged_df_by_sedol['Issue_Date']).dt.days
valid_prices_stage2 = merged_df_by_sedol[merged_df_by_sedol['days_difference'].between(-3, 60)].copy()
valid_prices_stage2['sorting_priority'] = np.where(
    valid_prices_stage2['days_difference'] >= 0, 
    valid_prices_stage2['days_difference'], 
    100 - valid_prices_stage2['days_difference']
)

best_matching_prices_stage2 = valid_prices_stage2.sort_values(
    ['original_row_index', 'sorting_priority']
).drop_duplicates(subset=['original_row_index'], keep='first')

unmapped_df = pd.merge(
    unmapped_df,
    best_matching_prices_stage2[['original_row_index', 'closing_price']],
    on='original_row_index',
    how='left'
)

unmapped_df['Underpricing'] = (unmapped_df['closing_price'] - unmapped_df['Offer_Price_USD']) / unmapped_df['Offer_Price_USD']
merged_df = pd.concat([mapped_df, unmapped_df], ignore_index=True).sort_values('original_row_index')


missing_count = merged_df['Underpricing'].isna().sum()
print(f"Number of firms missing Underpricing: {missing_count} / {len(merged_df)}")

merged_df = merged_df.drop(columns=['original_row_index', 'closing_price'])
merged_df['Issue_Date'] = merged_df['Issue_Date'].dt.strftime('%Y-%m-%d')

output_path = config.SECURITY_PRICE_OUTPUT
merged_df.to_stata(output_path, write_index=False)
merged_count = len(merged_df) - missing_count

print(f"A total of {len(merged_df)} rows were exported. This includes {merged_count} successful matches, along with {len(merged_df) - merged_count} unmapped rows.")
print(f"Exported to: {output_path}\n")

unmapped_firms = merged_df[merged_df['Underpricing'].isna()]

missing_isin = ~unmapped_firms['isin'].isin(security_df['isin'].dropna().unique())
missing_sedol = ~unmapped_firms['sedol'].isin(security_df['sedol'].dropna().unique())
missing_isin_and_sedol = (missing_isin & missing_sedol).sum()

date_mismatch_count = len(unmapped_firms) - missing_isin_and_sedol

print("--- Unmapped Reasons ---")
print(f"Total unmapped: {len(unmapped_firms)}")
print(f"1. ISIN and SEDOL not found in security database: {missing_isin_and_sedol}")
print(f"2. No trading records within date range: {date_mismatch_count}")