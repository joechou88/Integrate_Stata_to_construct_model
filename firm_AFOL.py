import pandas as pd
import config

print(f"Loading datasets:\n  - {config.IBES_NON_US_INPUT}\n  - {config.IBES_US_INPUT}\n  - {config.IBES_INT_INPUT}\n  - {config.COUNTRY_LEVEL_CONTROLS_OUTPUT}")
ibes_non_us = pd.read_sas(config.IBES_NON_US_INPUT, encoding="latin1")
ibes_us = pd.read_sas(config.IBES_US_INPUT, encoding="latin1")
ibes_int = pd.read_sas(config.IBES_INT_INPUT, encoding="latin1")
stata_df = pd.read_stata(config.COUNTRY_LEVEL_CONTROLS_OUTPUT)

ibes_df = pd.concat([ibes_us, ibes_non_us, ibes_int], ignore_index=True)

stata_df['year'] = stata_df['year'].fillna(0).astype(int)
ibes_df['year'] = ibes_df['fpe_year'].fillna(0).astype(int)

stata_df['sedol'] = stata_df['sedol'].astype(str).str.strip()
ibes_df['sedol'] = ibes_df['cusip'].astype(str).str.strip()

ibes_grouped = ibes_df.groupby(['sedol', 'year'])[['AFOL']].max().reset_index()
total_obs = len(stata_df)
merged_df = stata_df.merge(ibes_grouped, on=['sedol', 'year'], how='left')
merged_count = merged_df['AFOL'].notna().sum()

missing_counts = merged_df[merged_df['AFOL'].isna()].groupby(['sedol', 'year']).size().reset_index(name='Missing_Count')
with open("1-4_missing_AFOL_for_firm_year_combinations.txt", "w", encoding="utf-8") as f:
    f.write(missing_counts.to_string(index=False))

matched_counts = merged_df[merged_df['AFOL'].notna()].groupby(['sedol', 'year']).size().reset_index(name='Matched_Count')
with open("1-4_matched_AFOL_for_firm_year_combinations.txt", "w", encoding="utf-8") as f:
    f.write(matched_counts.to_string(index=False))

output_path = "IPO_2015_2019_with_firm_level_AFOL_0621.dta"
merged_df.to_stata(output_path, write_index=False)

print(f"A total of {len(merged_df)} rows were exported. This includes {merged_count} successful matches, along with {len(merged_df) - merged_count} unmapped rows.")
print(f"Exported to: {output_path}\n")