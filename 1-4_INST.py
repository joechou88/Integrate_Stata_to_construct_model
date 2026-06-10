import pandas as pd
import config

print(f"Loading datasets {config.INST_INPUT}, {config.AFOL_OUTPUT}")
inst_df = pd.read_sas(config.INST_INPUT, encoding="latin1")
stata_df = pd.read_stata(config.AFOL_OUTPUT)

inst_df.columns = inst_df.columns.str.lower()

print("Merging INST into Stata dataset...")

stata_df['sedol'] = stata_df['sedol'].astype(str).str.strip()
stata_df['Issue_Date'] = pd.to_datetime(stata_df['Issue_Date']).astype('datetime64[ns]')

inst_df['sedol'] = inst_df['sedol'].astype(str).str.strip()
inst_df['qtrdate'] = pd.to_datetime(inst_df['qtrdate']).astype('datetime64[ns]')

stata_df_sorted = stata_df.sort_values('Issue_Date')
inst_df_sorted = inst_df.dropna(subset=['sedol', 'qtrdate']).sort_values('qtrdate')

merged_df = pd.merge_asof(
    stata_df_sorted,
    inst_df_sorted[['sedol', 'qtrdate', 'valueheld', 'price', 'shrout', 'inst']],
    left_on='Issue_Date',
    right_on='qtrdate',
    by='sedol',
    direction='forward',
    tolerance=pd.Timedelta(days=180) # 往未來找最近的一個季底，但最多只找 180 天
)

merged_df['is_merged'] = merged_df['inst'].notna()
total_obs = len(stata_df)
unmatched_after = (~merged_df['is_merged']).sum()
merged_count = merged_df['is_merged'].sum()

print(f"Unmatched count after merging sedol: {unmatched_after} / {total_obs}")
missing_inst = merged_df[merged_df['inst'].isna()]
missing_details = missing_inst[['sedol', 'qtrdate', 'valueheld', 'price', 'shrout']].copy()
missing_details.rename(columns={'qtrdate': 'date'}, inplace=True)
missing_details.to_excel("1-4_missing_INST_firm_details.xlsx", index=False)

matched_inst = merged_df[merged_df['inst'].notna()]
matched_details = matched_inst[['sedol', 'qtrdate', 'valueheld', 'price', 'shrout', 'inst']].copy()
matched_details.rename(columns={'qtrdate': 'date'}, inplace=True)
matched_details.to_excel("1-4_matched_INST_firm_details.xlsx", index=False)

merged_df = merged_df.dropna(subset=['price', 'shrout'])

# 若 price / shrout 有，但 valueheld 缺 -> 代表純機構持股為 0，補 0
merged_df['valueheld'] = merged_df['valueheld'].fillna(0)
merged_df['inst'] = merged_df['inst'].fillna(0)

merged_df.rename(columns={'inst': 'INST'}, inplace=True)
merged_df['Issue_Date'] = merged_df['Issue_Date'].dt.strftime('%Y-%m-%d')
columns_to_drop = ['is_merged', 'qtrdate', 'valueheld', 'price', 'shrout']
merged_df = merged_df.drop(columns=[col for col in columns_to_drop if col in merged_df.columns])

output_filename = config.INST_OUTPUT
merged_df.to_stata(output_filename, write_index=False)

print(f"Original Stata row count: {total_obs}")
print(f"Total row count after merge: {len(merged_df)}")
print(f"Successfully matched sample count: {merged_count}")
print(f"Successfully exported to: {output_filename}")
