import pandas as pd
import numpy as np
import config

print(f"Loading datasets:\n  - {config.MARKET_PRICE_INPUT}\n  - {config.DERIVE_COLUMNS_OUTPUT}")
market_df = pd.read_csv(config.MARKET_PRICE_INPUT)
stata_df = pd.read_stata(config.DERIVE_COLUMNS_OUTPUT)

market_df['country_code'] = market_df['Country_code'].astype(str).str.strip().str.upper()
market_df['data_date'] = pd.to_datetime(market_df['datadate'], errors='coerce').dt.tz_localize(None)
market_df['daily_price'] = pd.to_numeric(market_df['prccd'], errors='coerce')

country_code_to_stock_index = {
    'ARG': 'Merval Index',
    'AUS': 'Australian All Ordinary Index',
    'AUT': 'ATX Index',
    'BEL': 'Belgium 20 Index',
    'BRA': 'Brazilian Bovespa Index',
    'CAN': 'MSCI - Canada Index (12/31/69)',         # Compustat does not have S&P/TSX Composite Index
    'COL': 'FTSE World Index - Colombia',            # Compustat does not have IGBC Index
    'DNK': 'OMX Copenhagen 20 Index',                # Formerly known as Copenhagen KFX Index
    'FIN': 'Helsinki General Index (HEX)',           # Later known as OMX Helsinki All-Share Index
    'FRA': 'SBF 120 Index',
    'DEU': 'HDAX',
    'GRC': 'Athens Stock Exchange General Index',
    'HKG': 'Hang Seng Index',
    'HUN': 'Budapest Stock Exchange Index',
    'ISR': 'Tel Aviv 100 Index',
    'ITA': 'BCI All-Share Index',
    'MYS': 'KLSE Composite Index',
    'MEX': 'IPC Index-Mexico',
    'NLD': 'Amsterdam AEX - Index',
    'NZL': 'New Zealand Stock Exchange 50 Index',
    'NOR': 'OSE All Share Index',                   # Compustat does not have Oslo Bors Benchmark Index
    'PAK': 'Karachi S.E 100 Share Index',
    'PER': 'Lima General Index',
    'PHL': 'Philippines SE Composite Index',
    'POL': 'Warsaw W.I.G Index',
    'PRT': 'Portugal BVL General Index',
    'SGP': 'Strait Times-Singapore Index',
    'KOR': 'Korea Stock Exchange Composite Index',
    'ESP': 'Madrid Stock Exchange Index',
    'SWE': 'OMX Stockholm 30 Index',
    'TWN': 'Taiwan Weighted Index',
    'THA': 'The Stock Exchange of Thailand (SET) Index',
    'TUR': 'ISE 100 Index-Turkey',
    'GBR': 'FTSE All-Share Index'
}

market_df = market_df.dropna(subset=['country_code', 'data_date', 'daily_price'])
market_df['target_index'] = market_df['country_code'].map(country_code_to_stock_index)
market_df = market_df[market_df['conm'] == market_df['target_index']]
market_df = market_df.sort_values(['country_code', 'data_date'])
market_df_by_country = market_df.groupby('country_code')

market_df['daily_return'] = market_df_by_country['daily_price'].pct_change()
market_df['Market_Volatility'] = market_df_by_country['daily_return'].transform(lambda x: x.rolling(21).std())
market_df['Market_Return'] = np.log(market_df['daily_price'] / market_df_by_country['daily_price'].shift(90))

market_df = market_df[['country_code', 'data_date', 'Market_Return', 'Market_Volatility']]
market_df = market_df.drop_duplicates(subset=['country_code', 'data_date'])
market_df = market_df.sort_values('data_date')

stata_df = stata_df.copy()

stata_df['original_index'] = stata_df.index
stata_df['country_code'] = stata_df['country_code2'].astype(str).str.strip().str.upper()
stata_df['target_merge_date'] = pd.to_datetime(stata_df['Issue_Date'], errors='coerce').dt.tz_localize(None) - pd.Timedelta(days=1)

valid_dates_data = stata_df.dropna(subset=['target_merge_date']).sort_values('target_merge_date')
missing_dates_data = stata_df[stata_df['target_merge_date'].isna()]

merged_valid_data = pd.merge_asof(
    valid_dates_data,
    market_df,
    left_on='target_merge_date',
    right_on='data_date',
    by='country_code',
    direction='backward'
)

merged_df = pd.concat([merged_valid_data, missing_dates_data], ignore_index=True)
merged_df = merged_df.sort_values('original_index')

columns_to_drop = ['original_index', 'country_code', 'target_merge_date', 'data_date']
merged_df = merged_df.drop(columns=columns_to_drop, errors='ignore')

output_path = config.MARKET_PRICE_OUTPUT
merged_df.to_stata(output_path, write_index=False)
merged_count = merged_df['Market_Return'].notna().sum()

print(f"A total of {len(merged_df)} rows were exported. This includes {merged_count} successful matches, along with {len(merged_df) - merged_count} unmapped rows.")
print(f"Exported to: {output_path}")
