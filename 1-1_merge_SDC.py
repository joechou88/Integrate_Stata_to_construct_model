import pandas as pd
import config

sdc_df = pd.read_excel(config.SDC_INPUT)
stata_df = pd.read_stata(config.OPERATING_LEASE_NPV_INPUT).copy()

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

# 第一輪：DSCD + Year
merged_df = pd.merge(sdc_df, stata_by_dscd, on=['dscd', 'year'], how='left', suffixes=('', '_stata'))
unmatched_after_dscd = merged_df['is_merged'].isna().sum()
print(f"1. DSCD+Year 合併後，未匹配數量: {unmatched_after_dscd} / {total_obs}")

# 第二輪：ISIN + Year
unmatched = merged_df['is_merged'].isna()
if unmatched.any():
    unmatched_part = merged_df[unmatched][sdc_df.columns]
    rematched_isin = pd.merge(unmatched_part, stata_by_isin, on=['isin', 'year'], how='left', suffixes=('', '_stata'))
    rematched_isin.index = unmatched_part.index
    merged_df.update(rematched_isin)

unmatched_after_isin = merged_df['is_merged'].isna().sum()
print(f"2. ISIN+Year 合併後，未匹配數量: {unmatched_after_isin} / {total_obs}")

# 第三輪：SEDOL + Year
unmatched = merged_df['is_merged'].isna()
if unmatched.any():
    unmatched_part_sedol = merged_df[unmatched][sdc_df.columns]
    unmatched_part_sedol = unmatched_part_sedol.dropna(subset=['sedol'])
    rematched_sedol = pd.merge(unmatched_part_sedol, stata_by_sedol, on=['sedol', 'year'], how='left', suffixes=('', '_stata'))
    rematched_sedol.index = unmatched_part_sedol.index
    merged_df.update(rematched_sedol)

unmatched_after_sedol = merged_df['is_merged'].isna().sum()
print(f"3. SEDOL+Year 合併後，最終未匹配數量: {unmatched_after_sedol} / {total_obs}")

for col in stata_df.columns:
    if f"{col}_stata" in merged_df.columns:
        merged_df[col] = merged_df[f"{col}_stata"]
        merged_df = merged_df.drop(columns=[f"{col}_stata"])

merged_count = merged_df['is_merged'].notna().sum()
merged_df = merged_df[merged_df['is_merged'].notna()].copy() # 沒有合併上的 record 就 drop 掉

if 'is_merged' in merged_df.columns:
    merged_df = merged_df.drop(columns=['is_merged'])

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

output_filename = config.SDC_OUTPUT
merged_df.to_stata(output_filename, write_index=False)

print(f"原始 Stata 行數: {total_obs}")
print(f"合併後總行數: {len(merged_df)}")
print(f"成功匹配樣本數量: {merged_count}")
print(f"成功導出至: {output_filename}")
