import pandas as pd
import config

print(f"Loading datasets:\n  - {config.SDC_INPUT}\n  - {config.NPV_LEASE_OUTPUT}\n  - {config.COUNTRY_CODE_INPUT}")
sdc_df = pd.read_excel(config.SDC_INPUT)
stata_df = pd.read_stata(config.NPV_LEASE_OUTPUT).copy()
country_code_df = pd.read_excel(config.COUNTRY_CODE_INPUT)

id_column_mapping = {
    'dscd': 'Datastream',
    'isin': 'ISIN',
    'sedol': 'Issuer/Borrower SEDOL',
}

for stata_col, sdc_col in id_column_mapping.items():
    stata_df[stata_col] = stata_df[stata_col].astype(str).str.strip().replace(['nan', 'None', ''], None)
    sdc_df[stata_col] = sdc_df[sdc_col].astype(str).str.strip().replace(['nan', 'None', ''], None)

stata_df['year'] = stata_df['year'].astype(int)
sdc_df['year'] = sdc_df['Dates: Offer Year (CCYY)'].astype(int)

stata_df['is_merged'] = 1
stata_by_dscd = stata_df.dropna(subset=['dscd']).drop_duplicates(subset=['dscd', 'year'])
stata_by_isin = stata_df.dropna(subset=['isin']).drop_duplicates(subset=['isin', 'year'])
stata_by_sedol = stata_df.dropna(subset=['sedol']).drop_duplicates(subset=['sedol', 'year'])
total_obs = len(sdc_df)
print(f"Original SDC rows in {config.SDC_INPUT}: {total_obs}")

# Round 1: DSCD + Year
merged_df = pd.merge(sdc_df, stata_by_dscd, on=['dscd', 'year'], how='left', suffixes=('', '_stata'))
unmatched_after_dscd = merged_df['is_merged'].isna().sum()
print(f"1. Unmatched after DSCD+Year: {unmatched_after_dscd} / {total_obs}")

# Round 2: ISIN + Year
unmatched = merged_df['is_merged'].isna()
if unmatched.any():
    unmatched_part = merged_df[unmatched][sdc_df.columns]
    rematched_isin = pd.merge(unmatched_part, stata_by_isin, on=['isin', 'year'], how='left', suffixes=('', '_stata'))
    rematched_isin.index = unmatched_part.index
    merged_df.update(rematched_isin)
unmatched_after_isin = merged_df['is_merged'].isna().sum()
print(f"2. Unmatched after ISIN+Year: {unmatched_after_isin} / {total_obs}")

# Round 3: SEDOL + Year
unmatched = merged_df['is_merged'].isna()
if unmatched.any():
    unmatched_part_sedol = merged_df[unmatched][sdc_df.columns].dropna(subset=['sedol'])
    rematched_sedol = pd.merge(unmatched_part_sedol, stata_by_sedol, on=['sedol', 'year'], how='left', suffixes=('', '_stata'))
    rematched_sedol.index = unmatched_part_sedol.index
    merged_df.update(rematched_sedol)
unmatched_after_sedol = merged_df['is_merged'].isna().sum()
print(f"3. Unmatched after SEDOL+Year: {unmatched_after_sedol} / {total_obs}")

# For overlapping columns (excluding dscd, isin, sedol, and year), prioritize Stata data over SDC.
for col in stata_df.columns:
    if f"{col}_stata" in merged_df.columns:
        if col not in ['dscd', 'isin', 'sedol', 'year']:
            merged_df[col] = merged_df[f"{col}_stata"]
            merged_df = merged_df.drop(columns=[f"{col}_stata"])

# Keep all SDC rows, instead of dropping unmatched rows.
merged_count = merged_df['is_merged'].notna().sum()
merged_df = merged_df.drop(columns=['is_merged']).copy()

merged_df['WS_country'] = merged_df['country']
# Update country codes based on SDC 'Country'
merged_df['country'] = merged_df['Country']
country_replacements = {
    'Hong-Kong': 'Hong Kong',
    'New-Zealand': 'New Zealand',
    'South-Korea': 'South Korea',
    'United-Kingdom': 'UK'
}
merged_df['country'] = merged_df['country'].replace(country_replacements)
merged_df['country_code'] = merged_df['country'].map(country_code_df.set_index('Country_name')['Country_code'])
merged_df['country_code2'] = merged_df['country'].map(country_code_df.set_index('Country_name')['Country_code2'])

added_columns = [
    'Underpricing', 'Ln_Age', 'VC_backed', 'Relative_Offer_Size',
    'Firm_Commitment', 'Underwriter_Reputation', 'Integer_Offer_Price',
    'Bookbuilt', 'IPO_count', 'Price_Stabilization', 'Equity_Carve_out',
    'Dates: Issue Date', 'Dates: Offer Year (CCYY)', 'Offer Price (USD)'
]

sdc_data = {}
for col in added_columns:
    if col in merged_df.columns:
        new_col = col.replace('Dates: ', '').replace(' ', '_').replace('/', '_').replace('-', '_').replace(':', '').replace('(', '').replace(')', '')
        sdc_data[new_col] = merged_df[col]

merged_df.columns = [c.replace(' ', '_').replace('/', '_').replace('-', '_').replace(':', '') for c in merged_df.columns]
original_stata_cols = [c for c in stata_df.columns if c in merged_df.columns]
original_stata_cols.insert(original_stata_cols.index('country'), 'WS_country')
merged_df = merged_df[original_stata_cols].copy()

insert_map = {
    'Underpricing': 21,
    'Ln_Age': 22,
    'Relative_Offer_Size': 110,
    'VC_backed': 115,
    'Firm_Commitment': 116,
    'Underwriter_Reputation': 117,
    'Integer_Offer_Price': 118,
    'Bookbuilt': 119,
    'Equity_Carve_out': 120,
    'IPO_count': 121, 
    'Price_Stabilization': 122,
    'Issue_Date': 123,
    'Offer_Year_CCYY': 124,
    'Offer_Price_USD': 125
}

for col, idx in sorted(insert_map.items(), key=lambda x: x[1]):
    if col in sdc_data:
        merged_df.insert(min(idx, len(merged_df.columns)), col, sdc_data[col])

output_path = config.SDC_OUTPUT
merged_df.to_stata(output_path, write_index=False)

print(f"A total of {len(merged_df)} rows were exported. This includes {merged_count} successful matches, along with {len(merged_df) - merged_count} unmapped rows.")
print(f"Exported to: {output_path}")
