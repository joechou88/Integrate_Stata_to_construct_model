import pandas as pd
import numpy as np
import config

print(f"Loading datasets:\n  - {config.SECURITY_PRICE_OUTPUT}\n  - {config.WORLDSCOPE_FUNDAMENTALS_INPUT}")
stata_df = pd.read_stata(config.SECURITY_PRICE_OUTPUT)
fundamental_df = pd.read_csv(config.WORLDSCOPE_FUNDAMENTALS_INPUT)

equity_counts = fundamental_df.groupby(['COUNTRY_CODE2', 'YEAR']).size().reset_index(name='listed_equities')
merged_df = stata_df.merge(
    equity_counts,
    left_on=['country_code2', 'year'], 
    right_on=['COUNTRY_CODE2', 'YEAR'], 
    how='left'
)
merged_df['IPO_count'] = np.log(merged_df['IPO_count'] / merged_df['listed_equities'])
merged_df['AFOL'] = merged_df['Total_AFOL'] / merged_df['listed_equities']
merged_df.rename(columns={'IPO_count': 'IPO_Activities'}, inplace=True)
merged_df.drop(columns=['COUNTRY_CODE2', 'YEAR', 'listed_equities'], inplace=True, errors='ignore')

output_path = config.WORLDSCOPE_EQUITY_COUNTS_OUTPUT
merged_df.to_stata(output_path, write_index=False)
print(f"Exported to: {output_path}\n")
