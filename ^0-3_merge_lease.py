import pandas as pd
import numpy as np
import config

print(f"Loading datasets:\n  - {config.LAG_OUTPUT}\n  - {config.NPV_LEASE_2000_2019}\n  - {config.ROU_2015_2024}")
stata_df = pd.read_stata(config.LAG_OUTPUT).copy()
npv_lease_df = pd.read_sas(config.NPV_LEASE_2000_2019, encoding="latin1")


output_path = config.NPV_LEASE_OUTPUT
merged_df.to_stata(output_path, write_index=False)
print(f"Exported to: {output_path}\n")
