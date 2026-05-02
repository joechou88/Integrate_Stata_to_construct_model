import pandas as pd
import config

sdc_df = pd.read_excel(config.SDC_INPUT)
stata_df = pd.read_stata(config.STATA_INPUT)

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

sdc_df['is_merged'] = 1
sdc_by_dscd = sdc_df.dropna(subset=['dscd']).drop_duplicates(subset=['dscd', 'year'])
sdc_by_isin = sdc_df.dropna(subset=['isin']).drop_duplicates(subset=['isin', 'year'])
sdc_by_sedol = sdc_df.dropna(subset=['sedol']).drop_duplicates(subset=['sedol', 'year'])
total_obs = len(stata_df)

# 第一輪：DSCD + Year
merged_df = pd.merge(stata_df, sdc_by_dscd, on=['dscd', 'year'], how='left', suffixes=('', '_sdc'))
unmatched_after_dscd = merged_df['is_merged'].isna().sum()
print(f"1. DSCD+Year 合併後，未匹配數量: {unmatched_after_dscd} / {total_obs}")

# 第二輪：ISIN + Year
unmatched = merged_df['is_merged'].isna()
if unmatched.any():
    unmatched_part = merged_df[unmatched][stata_df.columns]
    rematched_isin = pd.merge(unmatched_part, sdc_by_isin, on=['isin', 'year'], how='left', suffixes=('', '_drop'))
    merged_df.update(rematched_isin)

unmatched_after_isin = merged_df['is_merged'].isna().sum()
print(f"2. ISIN+Year 合併後，未匹配數量: {unmatched_after_isin} / {total_obs}")

# 第三輪：SEDOL + Year
unmatched = merged_df['is_merged'].isna()
if unmatched.any():
    unmatched_part_sedol = merged_df[unmatched][stata_df.columns]
    unmatched_part_sedol = unmatched_part_sedol.dropna(subset=['sedol'])
    sdc_df = sdc_df.dropna(subset=['sedol'])
    rematched_sedol = pd.merge(unmatched_part_sedol, sdc_by_sedol, on=['sedol', 'year'], how='left', suffixes=('', '_drop'))
    rematched_sedol.index = unmatched_part_sedol.index
    merged_df.update(rematched_sedol)

unmatched_after_sedol = merged_df['is_merged'].isna().sum()
print(f"3. SEDOL+Year 合併後，最終未匹配數量: {unmatched_after_sedol} / {total_obs}")

merged_df = merged_df.loc[:, ~merged_df.columns.str.contains('_drop')]
merged_count = merged_df['is_merged'].notna().sum()
if 'is_merged' in merged_df.columns:
    merged_df = merged_df.drop(columns=['is_merged'])
merged_df.columns = [c.replace(' ', '_').replace('/', '_').replace('-', '_').replace(':', '_') for c in merged_df.columns]

added_columns = [
    'Underpricing', 'Ln_Age', 'VC_backed', 'Relative_Offer_Size',
    'Firm_Commitment', 'Underwriter_Reputation', 'Integer_Offer_Price'
]
original_stata_cols = list(stata_df.columns)
output_columns = [col for col in (original_stata_cols + added_columns) if col in merged_df.columns]
merged_df = merged_df[output_columns]

output_filename = config.STATA_OUTPUT
merged_df.to_stata(output_filename, write_index=False)

print(f"原始 Stata 行數: {total_obs}")
print(f"合併後總行數: {len(merged_df)}")
print(f"成功匹配樣本數量: {merged_count}")
print(f"成功導出至: {output_filename}")
