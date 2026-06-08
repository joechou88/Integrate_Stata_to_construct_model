import pandas as pd
import config

print("Loading datasets...")
ibes_non_us = pd.read_sas(config.IBES_NON_US_INPUT, encoding="latin1")
ibes_us = pd.read_sas(config.IBES_US_INPUT, encoding="latin1")
ibes_int = pd.read_sas(config.IBES_INT_INPUT, encoding="latin1")
stata_df = pd.read_stata(config.STATA_COUNTRY_LEVEL_CONTROLS_OUTPUT)
ibes_df = pd.concat([ibes_us, ibes_non_us, ibes_int], ignore_index=True)
ibes_df.rename(columns={'cusip': 'sedol'}, inplace=True) # SAS 雖然看到 CUSIP/SEDOL，但 Python 讀出來是 cusip

stata_df['sedol'] = stata_df['sedol'].astype(str).str.strip().replace(['nan', 'None', ''], None)
ibes_df['sedol'] = ibes_df['sedol'].astype(str).str.strip().replace(['nan', 'None', ''], None)

stata_df['year'] = stata_df['year'].fillna(0).astype(int)
ibes_df['year'] = ibes_df['fpe_year'].fillna(0).astype(int)

ibes_by_sedol = ibes_df.dropna(subset=['sedol', 'year'])
ibes_by_sedol = ibes_by_sedol.groupby(['sedol', 'year'])[['AFOL']].mean().reset_index()

ibes_by_sedol['is_merged'] = 1
total_obs = len(stata_df)

print("Merging AFOL onto Stata dataset...")
merged_df = pd.merge(stata_df, ibes_by_sedol, on=['sedol', 'year'], how='left')

unmatched_after = merged_df['is_merged'].isna().sum()
merged_count = merged_df['is_merged'].notna().sum()
print(f"sedol+Year 合併後，未匹配數量: {unmatched_after} / {total_obs}")

missing_afol = merged_df[merged_df['AFOL'].isna()]
missing_counts = missing_afol.groupby(['sedol', 'year']).size().reset_index(name='Missing_IPO_Count')
missing_counts = missing_counts.sort_values(by=['sedol', 'year'])
with open("missing_AFOL_for_sedol_year_combinations.txt", "w", encoding="utf-8") as f:
    f.write(missing_counts.to_string(index=False))

matched_afol = merged_df[merged_df['AFOL'].notna()]
matched_counts = matched_afol.groupby(['sedol', 'year']).size().reset_index(name='Matched_IPO_Count')
matched_counts = matched_counts.sort_values(by=['sedol', 'year'])
with open("matched_AFOL_for_sedol_year_combinations.txt", "w", encoding="utf-8") as f:
    f.write(matched_counts.to_string(index=False))

if 'is_merged' in merged_df.columns:
    merged_df = merged_df.drop(columns=['is_merged'])

output_filename = config.STATA_AFOL_OUTPUT
merged_df.to_stata(output_filename, write_index=False)

print(f"原始 Stata 行數: {total_obs}")
print(f"合併後總行數: {len(merged_df)}")
print(f"成功匹配樣本數量: {merged_count}")
print(f"成功導出至: {output_filename}")