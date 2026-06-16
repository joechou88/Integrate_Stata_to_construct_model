import pandas as pd
import config
import numpy as np
import warnings

warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)

print(f"Loading datasets:\n  - {config.SME_OUTPUT}")
stata_df = pd.read_stata(config.SME_OUTPUT)

stata_df['Post'] = np.where((stata_df['year'] - 1) > 2018, 1, 0)
stata_df['PostxHigh_Lease'] = stata_df['Post'] * stata_df['high_lease']
stata_df = stata_df.rename(columns={'high_lease': 'High_Lease'})

insert_map = {
    'Post': 22,
    'High_Lease': 23,
    'PostxHigh_Lease': 24
}

for col, idx in sorted(insert_map.items(), key=lambda x: x[1]):
    if col in stata_df.columns:
        col_series = stata_df.pop(col)
        actual_idx = min(idx, len(stata_df.columns))
        stata_df.insert(actual_idx, col, col_series)
        print(f"Moved column '{col}' to index {actual_idx}")

stata_df = stata_df.copy()

output_path = config.DERIVE_COLUMNS_OUTPUT
stata_df.to_stata(output_path, write_index=False)
print(f"Exported to: {output_path}")
