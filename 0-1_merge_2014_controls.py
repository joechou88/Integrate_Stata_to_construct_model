import pandas as pd
import config

print(f"Loading datasets:\n  - {config.LEASE_NPV_INPUT_2015_2024}\n  - {config.CONTROLS_INPUT_1996_2019}")
stata_df = pd.read_stata(config.LEASE_NPV_INPUT_2015_2024).copy()
sas_df = pd.read_sas(config.CONTROLS_INPUT_1996_2019, encoding="latin1")

records_2014 = sas_df[sas_df['year'] == 2014].copy()
existing_stata_columns = stata_df.columns.intersection(records_2014.columns)
records_2014 = records_2014[existing_stata_columns]
merged_df = pd.concat([stata_df, records_2014], ignore_index=True)
merged_df = merged_df[stata_df.columns]

output_path = config.LEASE_NPV_OUTPUT_2014_2024
merged_df.to_stata(output_path, write_index=False)
print(f"Exported to: {output_path}")
