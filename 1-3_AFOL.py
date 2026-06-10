import pandas as pd
import config

ibes_non_us = pd.read_sas(config.IBES_NON_US_INPUT, encoding="latin1")
ibes_us = pd.read_sas(config.IBES_US_INPUT, encoding="latin1")
ibes_int = pd.read_sas(config.IBES_INT_INPUT, encoding="latin1")
stata_df = pd.read_stata(config.COUNTRY_LEVEL_CONTROLS_OUTPUT)
ibes_df = pd.concat([ibes_us, ibes_non_us, ibes_int], ignore_index=True)

stata_df['country'] = stata_df['country'].astype(str).str.strip()
ibes_df['country'] = ibes_df['country'].astype(str).str.strip()

stata_df['year'] = stata_df['year'].fillna(0).astype(int)
ibes_df['year'] = ibes_df['fpe_year'].fillna(0).astype(int)

country_name_mapping = {
    'Korea': 'South Korea',
    'United Kingdom': 'UK'
}
ibes_df['country'] = ibes_df['country'].replace(country_name_mapping)

ibes_by_country = ibes_df.dropna(subset=['country', 'year'])
ibes_by_country = ibes_by_country.groupby(['country', 'year'])[['AFOL']].mean().reset_index()

ibes_by_country['is_merged'] = 1
total_obs = len(stata_df)

print("Merging AFOL onto Stata dataset...")
merged_df = pd.merge(stata_df, ibes_by_country, on=['country', 'year'], how='left')

unmatched_after = merged_df['is_merged'].isna().sum()
merged_count = merged_df['is_merged'].notna().sum()
print(f"country_code+Year 合併後，未匹配數量: {unmatched_after} / {total_obs}")

missing_afol = merged_df[merged_df['AFOL'].isna()]
missing_counts = missing_afol.groupby(['country', 'year']).size().reset_index(name='Missing_IPO_Count')
missing_counts = missing_counts.sort_values(by=['country', 'year'])
with open("1-3_missing_AFOL_for_country_year_combinations.txt", "w", encoding="utf-8") as f:
    f.write(missing_counts.to_string(index=False))

matched_afol = merged_df[merged_df['AFOL'].notna()]
matched_counts = matched_afol.groupby(['country', 'year']).size().reset_index(name='Matched_IPO_Count')
matched_counts = matched_counts.sort_values(by=['country', 'year'])
with open("1-3_matched_AFOL_for_country_year_combinations.txt", "w", encoding="utf-8") as f:
    f.write(matched_counts.to_string(index=False))

if 'is_merged' in merged_df.columns:
    merged_df = merged_df.drop(columns=['is_merged'])

output_filename = config.AFOL_OUTPUT
merged_df.to_stata(output_filename, write_index=False)

print(f"原始 Stata 行數: {total_obs}")
print(f"合併後總行數: {len(merged_df)}")
print(f"成功匹配樣本數量: {merged_count}")
print(f"成功導出至: {output_filename}")