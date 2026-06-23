import pandas as pd
import config

print(f"Loading datasets:\n  - {config.COUNTRY_LEVEL_CONTROLS_INPUT}\n  - {config.OFFER_PRICE_OUTPUT}")
excel_raw = pd.read_excel(config.COUNTRY_LEVEL_CONTROLS_INPUT)
stata_df = pd.read_stata(config.OFFER_PRICE_OUTPUT)

excel_raw.columns = excel_raw.columns.str.replace(" ", "_")
excel_raw = excel_raw.rename(columns={
    'Country_code': 'country_code', 
    'Year': 'year',
    'Overall_Score': 'Economic_Freedom'
})

primary_keys = ["country_code", "year"]
control_columns = [
    'Economic_Freedom', 'GDP_per_capita_US', 'Ln_GDPOP', 
    'GDP_per_capita_growth', 'Land_area', 'Listed_domestic_companies', 
    'Ln_Listed', 'CAP_Ratio', 'str'
]

control_df = excel_raw[primary_keys + control_columns].copy()

for col in control_columns + ['year']:
    control_df[col] = pd.to_numeric(control_df[col], errors='coerce')
control_df['country_code'] = control_df['country_code'].astype(str).str.strip()

# Keep first instance of duplicated keys
control_df = control_df.drop_duplicates(subset=primary_keys, keep='first')

# Forward fill Hong Kong 2020 Economic_Freedom to 2021-2024
hk_2020_score = control_df.loc[(control_df['country_code'] == 'HK') & (control_df['year'] == 2020), 'Economic_Freedom']
if not hk_2020_score.empty:
    hk_2020_score = hk_2020_score.values[0]
    hk_mask = (control_df['country_code'] == 'HK') & (control_df['year'].isin([2021, 2022, 2023, 2024]))
    control_df.loc[hk_mask, 'Economic_Freedom'] = hk_2020_score
    print(f"Filled Hong Kong 2020 Economic Freedom {hk_2020_score} in 2021~2024. {hk_mask.sum()} rows affected.")

stata_df['country_code'] = stata_df['country_code'].astype(str).str.strip()
stata_df['year'] = pd.to_numeric(stata_df['year'], errors='coerce')

overlap_columns = [c for c in control_columns if c in stata_df.columns]
stata_df = stata_df.drop(columns=overlap_columns)

merged_df = pd.merge(stata_df, control_df, on=primary_keys, how='left')

output_path = config.COUNTRY_LEVEL_CONTROLS_OUTPUT
merged_df.to_stata(output_path, write_index=False)
merged_count = merged_df[control_columns[0]].notna().sum()

print(f"A total of {len(merged_df)} rows were exported. This includes {merged_count} successful matches, along with {len(merged_df) - merged_count} unmapped rows.")
print(f"Exported to: {output_path}\n")
