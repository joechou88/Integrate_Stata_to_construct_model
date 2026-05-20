import pandas as pd
import config
import warnings

warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)

input_path = config.STATA_DERIVE_COLUMNS_OUTPUT
print(f"Reading data from {input_path}...")
df = pd.read_stata(input_path)

target_col_high = 'high_lease'
target_idx_high = 23

if target_col_high in df.columns:
    col_series = df.pop(target_col_high)
    actual_idx_high = min(target_idx_high, len(df.columns))
    df.insert(actual_idx_high, target_col_high, col_series)
    print(f"Moved '{target_col_high}' to index {actual_idx_high}")
else:
    print(f"[WARN] Column '{target_col_high}' not found in the dataset.")

if 'Post' in df.columns and 'high_lease' in df.columns:
    interaction_name = 'Postxhigh_lease'
    interaction_series = df['Post'] * df['high_lease']
    
    target_idx_interaction = 24
    actual_idx_interaction = min(target_idx_interaction, len(df.columns))
    
    df.insert(actual_idx_interaction, interaction_name, interaction_series)
    print(f"Inserted '{interaction_name}' at index {actual_idx_interaction}")
else:
    print("[Error] Could not calculate interaction. Check if 'Post' and 'high_lease' exist.")

df = df.copy()

output_path = config.STATA_Model1_OUTPUT
print(f"Saving to {output_path}...")

try:
    df.to_stata(output_path, write_index=False)
    print(f"[OK] Model 1 data prepared and saved successfully.")
except Exception as e:
    print(f"[Error] Failed to save Stata file: {e}")