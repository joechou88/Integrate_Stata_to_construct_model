import pandas as pd
import numpy as np
import config

print(f"Loading datasets:\n  - {config.FILTERED_OUTPUT}")
stata_df = pd.read_stata(config.FILTERED_OUTPUT)
lease_df = pd.read_csv(config.ORIGIN_LEASE_2000_2019)

lease_df['missing_lease_condition'] = (
    (lease_df['lc_year1'] == 0) &
    (lease_df['lc_year2'] == 0) &
    (lease_df['lc_year3'] == 0) &
    (lease_df['lc_year4'] == 0) &
    (lease_df['lc_year5'] == 0) &
    (lease_df['lc_over5year'].isna())
)

stata_df = stata_df.merge(
    lease_df[['sedol', 'missing_lease_condition']].drop_duplicates(), 
    on='sedol', 
    how='left'
)

stata_df['missing_lease_condition'] = stata_df['missing_lease_condition'].fillna(False)
stata_df['orig_lease_intensity_pre'] = stata_df['lease_intensity_pre']
print(f"Rows changed from 0 to missing (.): {stata_df['missing_lease_condition'].sum()}")
stata_df.loc[stata_df['missing_lease_condition'] == True, 'orig_lease_intensity_pre'] = np.nan
stata_df.drop(columns=['missing_lease_condition'], inplace=True)

target_column_index = stata_df.columns.get_loc('lease_intensity_pre') + 1
column_to_insert = stata_df.pop('orig_lease_intensity_pre')
stata_df.insert(target_column_index, 'orig_lease_intensity_pre', column_to_insert)

output_path = config.MARK_OUTPUT
stata_df.to_stata(output_path, write_index=False)
print(f"Exported to: {output_path}\n")
