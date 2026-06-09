import pandas as pd
import config

print(f"Loading datasets {config.OWNER_INFO_INPUT}, {config.CONSOLIDATED_HOLDINGS_INPUT}, {config.OWNER_PRICE_INPUT}, {config.STATA_AFOL_OUTPUT}")
owner_info = pd.read_sas(config.OWNER_INFO_INPUT, encoding="latin1")
owner_price = pd.read_sas(config.OWNER_PRICE_INPUT, encoding="latin1")
holdings = pd.read_sas(config.CONSOLIDATED_HOLDINGS_INPUT, encoding="latin1")
stata_df = pd.read_stata(config.STATA_AFOL_OUTPUT)

stata_df['sedol'] = stata_df['sedol'].astype(str).str.strip()
stata_df['Issue_Date'] = pd.to_datetime(stata_df['Issue_Date'])

print("Step 1: Filtering for pure institutional investors...")
merged_holdings = pd.merge(holdings, owner_info, on='ownercode', how='left')
merged_holdings['owntypecode'] = pd.to_numeric(merged_holdings['owntypecode'], errors='coerce')
strategic_codes = [301, 302, 303, 304]
pure_inst_holdings = merged_holdings[~merged_holdings['owntypecode'].isin(strategic_codes)].copy()

print("Step 2: Calculating INST numerator (Value held by institutional investors)...")
# Get issuercode from owner_price using securitycode
security_issuer_mapping = owner_price[['securitycode', 'issuercode']].dropna().drop_duplicates()
pure_inst_holdings = pd.merge(pure_inst_holdings, security_issuer_mapping, on='securitycode', how='left')

inst_numerator = pure_inst_holdings.groupby(['issuercode', 'qtrdate'])['valueheld'].sum().reset_index()
inst_numerator.rename(columns={'valueheld': 'total_valueheld'}, inplace=True)

print("Step 3: Calculating INST denominator (Market Cap)...")
owner_price['marketcap_temp'] = owner_price['price'] * owner_price['shrout']
inst_denominator = owner_price.groupby(['issuercode', 'date'])['marketcap_temp'].max().reset_index()
inst_denominator.rename(columns={'marketcap_temp': 'marketcap'}, inplace=True)

print("Step 4: Calculating INST...")
inst_denominator.rename(columns={'date': 'qtrdate'}, inplace=True)
inst_df = pd.merge(inst_numerator, inst_denominator, on=['issuercode', 'qtrdate'], how='inner')
inst_df['INST'] = inst_df['total_valueheld'] / inst_df['marketcap']

print("Step 5: Merging INST into Stata dataset...")
sedol_mapping = owner_price[['issuercode', 'sedol']].dropna().drop_duplicates()
inst_df = pd.merge(inst_df, sedol_mapping, on='issuercode', how='left')
inst_df['sedol'] = inst_df['sedol'].astype(str).str.strip()
inst_df['qtrdate'] = pd.to_datetime(inst_df['qtrdate'])

stata_df_sorted = stata_df.sort_values('Issue_Date')
inst_df_sorted = inst_df.dropna(subset=['sedol', 'qtrdate']).sort_values('qtrdate')

merged_df = pd.merge_asof(
    stata_df_sorted,
    inst_df_sorted[['sedol', 'qtrdate', 'INST']],
    left_on='Issue_Date',
    right_on='qtrdate',
    by='sedol',
    direction='forward'
)

merged_df['is_merged'] = merged_df['INST'].notna()
total_obs = len(stata_df)
unmatched_after = (~merged_df['is_merged']).sum()
merged_count = merged_df['is_merged'].sum()

print(f"Unmatched count after merging sedol: {unmatched_after} / {total_obs}")
missing_inst = merged_df[merged_df['INST'].isna()]
missing_counts = missing_inst.groupby(['sedol']).size().reset_index(name='Missing_INST_Count')
missing_counts = missing_counts.sort_values(by=['sedol'])
with open("1-4_missing_INST.txt", "w", encoding="utf-8") as f:
    f.write(missing_counts.to_string(index=False))

matched_inst = merged_df[merged_df['INST'].notna()]
matched_counts = matched_inst.groupby(['sedol']).size().reset_index(name='Matched_INST_Count')
matched_counts = matched_counts.sort_values(by=['sedol'])
with open("1-4_matched_INST.txt", "w", encoding="utf-8") as f:
    f.write(matched_counts.to_string(index=False))

columns_to_drop = ['is_merged']
merged_df = merged_df.drop(columns=[col for col in columns_to_drop if col in merged_df.columns])

output_filename = config.STATA_INST_OUTPUT
merged_df.to_stata(output_filename, write_index=False)

print(f"Original Stata row count: {total_obs}")
print(f"Total row count after merge: {len(merged_df)}")
print(f"Successfully matched sample count: {merged_count}")
print(f"Successfully exported to: {output_filename}")
