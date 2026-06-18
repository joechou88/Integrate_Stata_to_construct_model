import pandas as pd
import numpy as np
import config

print(f"Loading datasets:\n  - {config.LAG_OUTPUT}\n  - {config.NPV_LEASE_2000_2019}\n  - {config.ROU_2015_2024}")
stata_df = pd.read_stata(config.LAG_OUTPUT).copy()
npv_lease_df = pd.read_sas(config.NPV_LEASE_2000_2019, encoding="latin1")
rou_df = pd.read_sas(config.ROU_2015_2024, encoding="latin1")

rou_df = rou_df.rename(columns={'ROU_Tang_Total': 'rou_tang_total', 'DSCD': 'dscd', 'YEAR': 'year'})
rou_df['rou_at'] = rou_df['rou_tang_total'] / rou_df['Total_assets']

npv_lease_df['year'] = npv_lease_df['year'] + 1
rou_df['year'] = rou_df['year'] + 1

cols_to_update = ['npv_lease', 'rou_tang_total', 'rou_at']
existing_cols = [col for col in cols_to_update if col in stata_df.columns]
if existing_cols:
    stata_df = stata_df.drop(columns=existing_cols)

merged_df = stata_df.merge(npv_lease_df[['dscd', 'year', 'npv_lease']], on=['dscd', 'year'], how='left')
merged_df = merged_df.merge(rou_df[['dscd', 'year', 'rou_tang_total', 'rou_at']], on=['dscd', 'year'], how='left')
merged_df['leasenpv_at'] = merged_df['npv_lease'] / merged_df['total_assets']

merged_df['Lease_Intensity'] = np.where(
    merged_df['year'] <= 2019,
    merged_df['leasenpv_at'],   # 2015~2019 IPO uses lagged LeaseNPV_AT
    merged_df['rou_at']         # 2020~2024 IPO uses lagged rou_at
)

group_median = merged_df.groupby(['year', 'country_code2', 'sic2digit'])['Lease_Intensity'].transform('median')
merged_df['High_Lease2'] = np.where(
    merged_df['Lease_Intensity'].isna(),
    np.nan,  # Keep missing values as NaN
    (merged_df['Lease_Intensity'] > group_median).astype(float)
)

missing_dscd = merged_df[merged_df['Lease_Intensity'].isna()]['dscd'].unique()
missing_npv_records = npv_lease_df[npv_lease_df['dscd'].isin(missing_dscd) & npv_lease_df['year'].between(2015, 2024)][['dscd', 'year', 'npv_lease']]
missing_rou_records = rou_df[rou_df['dscd'].isin(missing_dscd) & rou_df['year'].between(2015, 2024)][['dscd', 'year', 'rou_tang_total', 'rou_at']]

with pd.ExcelWriter("0-3_missing_lease.xlsx") as writer:
    missing_npv_records.to_excel(writer, sheet_name="Missing_NPV", index=False)
    missing_rou_records.to_excel(writer, sheet_name="Missing_ROU", index=False)

output_path = config.NPV_LEASE_OUTPUT
merged_df.to_stata(output_path, write_index=False)
print(f"Exported to: {output_path}")
