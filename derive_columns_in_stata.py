import pandas as pd
import config
import numpy as np
import warnings

warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)

input_path = config.STATA_COUNTRY_LEVEL_CONTROLS_OUTPUT
print(f"Reading data from {input_path}...")
df = pd.read_stata(input_path)

df['Post'] = np.where((df['year'] - 1) > 2018, 1, 0)
df['Postxhigh_lease'] = df['Post'] * df['high_lease']

insert_map = {
    'Post': 22,
    'Postxhigh_lease': 23
}

for col, idx in sorted(insert_map.items(), key=lambda x: x[1]):
    if col in df.columns:
        col_series = df.pop(col)
        actual_idx = min(idx, len(df.columns))
        df.insert(actual_idx, col, col_series)
        print(f"Moved column '{col}' to index {actual_idx}")

df = df.copy()

output_path = config.STATA_DERIVE_COLUMNS_OUTPUT
print(f"Saving to {output_path}...")

try:
    df.to_stata(output_path, write_index=False)
    print("[OK] Columns derived and file saved successfully.")
except Exception as e:
    print(f"[Error] Failed to save Stata file: {e}")