import pandas as pd
import numpy as np
import duckdb
import config

print(f"Loading datasets:\n  - {config.MARKET_PRICE_OUTPUT}\n  - {config.SECURITY_PRICE_INPUT}")
stata_df = pd.read_stata(config.MARKET_PRICE_OUTPUT)
stata_df['Issue_Date'] = pd.to_datetime(stata_df['Issue_Date'])
stata_df = stata_df.reset_index(names='original_row_index')

query = f"""
    SELECT isin, sedol, datadate AS closing_price_date, prccd AS closing_price
    FROM '{config.SECURITY_PRICE_INPUT}'
    WHERE prccd IS NOT NULL
      AND (
          isin IN (SELECT isin FROM stata_df WHERE isin IS NOT NULL)
          OR 
          sedol IN (SELECT sedol FROM stata_df WHERE sedol IS NOT NULL)
      )
"""
security_df = duckdb.query(query).to_df()
security_df['closing_price_date'] = pd.to_datetime(security_df['closing_price_date'])
security_df = security_df.drop_duplicates(subset=['isin', 'sedol', 'closing_price_date'], keep='last')

matched_firms = []
unmapped_firms = stata_df.copy()

for id in ['isin', 'sedol']:
    temp_merged = pd.merge(
        unmapped_firms[['original_row_index', id, 'Issue_Date']], 
        security_df.dropna(subset=[id]), 
        on=id, 
        how='inner'
    )
    temp_merged['days_difference'] = (temp_merged['closing_price_date'] - temp_merged['Issue_Date']).dt.days
    valid_window = temp_merged[temp_merged['days_difference'].between(-3, 60)].copy()

    valid_window['sorting_priority'] = np.where(
        valid_window['days_difference'] >= 0, 
        valid_window['days_difference'], 
        100 - valid_window['days_difference']
    )

    best_prices = valid_window.sort_values(['original_row_index', 'sorting_priority'])\
                              .drop_duplicates(subset=['original_row_index'], keep='first')
    matched_firms.append(best_prices)
    unmapped_firms = unmapped_firms[~unmapped_firms['original_row_index'].isin(best_prices['original_row_index'])]

all_best_prices = pd.concat(matched_firms) if matched_firms else pd.DataFrame()
merged_df = pd.merge(
    stata_df,
    all_best_prices[['original_row_index', 'closing_price', 'closing_price_date']],
    on='original_row_index',
    how='left'
)
merged_df['Underpricing'] = (merged_df['closing_price'] - merged_df['Offer_Price_Local']) / merged_df['Offer_Price_Local']

missing_count = merged_df['Underpricing'].isna().sum()
print(f"Number of firms missing Underpricing: {missing_count} / {len(merged_df)}")

merged_df = merged_df.drop(columns=['original_row_index'])
merged_df['Issue_Date'] = merged_df['Issue_Date'].dt.strftime('%Y-%m-%d')
merged_df['closing_price_date'] = merged_df['closing_price_date'].dt.strftime('%Y-%m-%d')

output_path = config.SECURITY_PRICE_OUTPUT
merged_df.to_stata(output_path, write_index=False)
merged_count = len(merged_df) - missing_count

print(f"A total of {len(merged_df)} rows were exported. This includes {merged_count} successful matches, along with {len(merged_df) - merged_count} unmapped rows.")
print(f"Exported to: {output_path}")

missing_isin = ~unmapped_firms['isin'].isin(security_df['isin'].dropna().unique())
missing_sedol = ~unmapped_firms['sedol'].isin(security_df['sedol'].dropna().unique())
missing_isin_and_sedol = (missing_isin & missing_sedol).sum()
date_mismatch_count = len(unmapped_firms) - missing_isin_and_sedol

print(f"--- Unmapped reasons for {len(unmapped_firms)} firms ---")
print(f"1. ISIN and SEDOL not found in security database: {missing_isin_and_sedol}")
print(f"2. No trading records within date range (-3, +60): {date_mismatch_count}\n")
