import pandas as pd
import config
import warnings

warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)

input_path = config.STATA_DERIVE_COLUMNS_OUTPUT
print(f"Reading data from {input_path}...")
df = pd.read_stata(input_path)

move_map = {
    'high_lease': 23,
    'Underwriter_Reputation': 24
}

for col, target_idx in move_map.items():
    if col in df.columns:
        col_series = df.pop(col)
        actual_idx = min(target_idx, len(df.columns))
        df.insert(actual_idx, col, col_series)
        print(f"Moved '{col}' to index {actual_idx}")

if all(k in df.columns for k in ['Post', 'high_lease', 'Underwriter_Reputation']):
    interactions = [
        ('postxhigh_lease', df['Post'] * df['high_lease'], 25),
        ('postxUW_Reputation', df['Post'] * df['Underwriter_Reputation'], 26),
        ('high_leasexUW_Reputation', df['high_lease'] * df['Underwriter_Reputation'], 27),
        ('postxhigh_leasexUW_Reputation', df['Post'] * df['high_lease'] * df['Underwriter_Reputation'], 28)
    ]
    
    for name, series, target_idx in interactions:
        actual_idx = min(target_idx, len(df.columns))
        df.insert(actual_idx, name, series)
        print(f"Inserted '{name}' at index {actual_idx}")
else:
    print("[Error] Missing required variables (Post, high_lease, or Underwriter_Reputation).")

df = df.copy()

output_path = config.STATA_Model2_OUTPUT
print(f"Saving to {output_path}...")

try:
    df.to_stata(output_path, write_index=False)
    print(f"[OK] Model 2 data prepared and saved successfully.")
except Exception as e:
    print(f"[Error] Failed to save Stata file: {e}")
