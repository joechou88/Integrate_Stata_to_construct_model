import pandas as pd

start_year = 2015
end_year = 2022

input_path = f"Stata/IPO_{start_year}_{end_year}_filtered.dta"
print(f"Loading datasets:\n  - {input_path}")
stata_df = pd.read_stata(input_path)

stata_df = stata_df[stata_df['year'].between(start_year, end_year)]
row_count_before_drop = len(stata_df)
stata_df = stata_df.dropna()
row_count_after_drop = len(stata_df)

print(f"Statistics for year range: {start_year} to {end_year}")
print(f"Rows before dropping missing values: {row_count_before_drop}")
print(f"Rows after dropping missing values: {row_count_after_drop}")
print(f"Total rows dropped: {row_count_before_drop - row_count_after_drop}")

output_path = f"Stata/IPO_{start_year}_{end_year}_remove_missing.dta"
stata_df.to_stata(output_path, write_index=False)
print(f"Exported to: {output_path}\n")
