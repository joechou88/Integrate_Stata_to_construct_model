import pandas as pd
import config

print("Loading datasets...")
ibes_non_us = pd.read_sas(config.IBES_NON_US_INPUT, encoding="latin1")
ibes_us = pd.read_sas(config.IBES_US_INPUT, encoding="latin1")
ibes_int = pd.read_sas(config.IBES_INT_INPUT, encoding="latin1")
stata_df = pd.read_stata(config.STATA_COUNTRY_LEVEL_CONTROLS_OUTPUT)
ibes_df = pd.concat([ibes_us, ibes_non_us, ibes_int], ignore_index=True)

stata_df['country_code'] = stata_df['country_code'].astype(str).str.strip().replace(['nan', 'None', ''], None)
ibes_df['country_code'] = ibes_df['country_code'].astype(str).str.strip().replace(['nan', 'None', ''], None)

stata_df['year'] = stata_df['year'].fillna(0).astype(int)
ibes_df['year'] = ibes_df['fpe_year'].fillna(0).astype(int)

ibes_by_country = ibes_df.dropna(subset=['country_code', 'year'])
ibes_by_country = ibes_by_country.groupby(['country_code', 'year'])[['AFOL', 'Ln_AFOL']].mean().reset_index()

ibes_by_country['is_merged'] = 1
total_obs = len(stata_df)

print("Merging AFOL onto Stata dataset...")
merged_df = pd.merge(stata_df, ibes_by_country, on=['country_code', 'year'], how='left')

unmatched_after = merged_df['is_merged'].isna().sum()
merged_count = merged_df['is_merged'].notna().sum()
print(f"country_code+Year 合併後，未匹配數量: {unmatched_after} / {total_obs}")

missing_afol = merged_df[merged_df['AFOL'].isna()]
missing_counts = missing_afol.groupby(['country', 'country_code', 'year']).size().reset_index(name='Missing_IPO_Count')
missing_counts = missing_counts.sort_values(by=['country', 'year'])

with open("missing_AFOL_for_country_year_combinations.txt", "w", encoding="utf-8") as f:
    f.write(missing_counts.to_string(index=False))

if 'is_merged' in merged_df.columns:
    merged_df = merged_df.drop(columns=['is_merged'])

output_filename = config.STATA_AFOL_OUTPUT
merged_df.to_stata(output_filename, write_index=False)

print(f"原始 Stata 行數: {total_obs}")
print(f"合併後總行數: {len(merged_df)}")
print(f"成功匹配樣本數量: {merged_count}")
print(f"成功導出至: {output_filename}")