import pandas as pd
import config

print(f"Loading datasets:\n  - {config.INST_INPUT}\n  - {config.AFOL_OUTPUT}")
inst_df = pd.read_sas(config.INST_INPUT, encoding="latin1")
stata_df = pd.read_stata(config.AFOL_OUTPUT)

inst_df.columns = inst_df.columns.str.lower()
stata_df['sedol'] = stata_df['sedol'].astype(str).str.strip()
inst_df['sedol'] = inst_df['sedol'].astype(str).str.strip()
stata_df['Issue_Date'] = pd.to_datetime(stata_df['Issue_Date']).astype('datetime64[ns]')
inst_df['qtrdate'] = pd.to_datetime(inst_df['qtrdate']).astype('datetime64[ns]')
stata_df = stata_df.sort_values('Issue_Date')

inst_fallback = inst_df.dropna(subset=['sedol', 'qtrdate', 'price', 'shrout']).sort_values('qtrdate')
inst_priority = inst_fallback.dropna(subset=['valueheld'])

merge_columns = ['sedol', 'qtrdate', 'valueheld', 'price', 'shrout', 'inst']
# Look forward to the next quarter-end, max 180 days
merge_kwargs = dict(left_on='Issue_Date', right_on='qtrdate', by='sedol', direction='forward', tolerance=pd.Timedelta(days=180))

df_priority = pd.merge_asof(stata_df, inst_priority[merge_columns], **merge_kwargs)
df_fallback = pd.merge_asof(stata_df, inst_fallback[merge_columns], **merge_kwargs)
merged_df = df_priority.fillna(df_fallback)

# If price and shrout exists but valueheld is missing, fill with 0
mask_zero = merged_df['price'].notna() & merged_df['shrout'].notna() & merged_df['valueheld'].isna()
merged_df.loc[mask_zero, ['valueheld', 'inst']] = 0

columns = ['sedol', 'Issue_Date', 'qtrdate', 'valueheld', 'price', 'shrout', 'inst']
merged_df[merged_df['inst'].isna()][columns].to_excel("1-5_missing_INST.xlsx", index=False)
merged_df[merged_df['inst'].notna()][columns].to_excel("1-5_matched_INST.xlsx", index=False)

merged_df.rename(columns={'inst': 'INST'}, inplace=True)
merged_df['Issue_Date'] = merged_df['Issue_Date'].dt.strftime('%Y-%m-%d')
merged_df.drop(columns=['qtrdate', 'valueheld', 'price', 'shrout'], inplace=True, errors='ignore')
merged_count = merged_df['INST'].notna().sum()

output_path = config.INST_OUTPUT
merged_df.to_stata(output_path, write_index=False)

print(f"A total of {len(merged_df)} rows were exported. This includes {merged_count} successful matches, along with {len(merged_df) - merged_count} unmapped rows.")
print(f"Exported to: {output_path}\n")
