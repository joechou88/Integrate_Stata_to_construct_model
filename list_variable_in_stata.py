import pandas as pd
import os

folder = "Stata"
stata_files = [
    "Financial_npv_lease20152024.dta",
    "Financial_npv_lease20152024_20260428.dta",
    "Financial_npv_lease20152024_20260501.dta"
]

def get_stata_headers(file_list, folder_path):
    headers_dict = {}
    
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        try:
            # Efficiently read only the metadata
            with pd.read_stata(file_path, chunksize=1) as reader:
                for chunk in reader:
                    headers_dict[file_name] = list(chunk.columns)
                    break
        except FileNotFoundError:
            print(f"Error: {file_path} not found.")
        except Exception as e:
            print(f"An error occurred with {file_name}: {e}")        
    return headers_dict

def compare_headers(headers_dict):
    files = list(headers_dict.keys())
    if len(files) < 2:
        print("Not enough files found to compare.")
        return

    baseline_file = files[0]
    baseline_cols = set(headers_dict[baseline_file])
    print(f"Baseline File: {baseline_file} ({len(baseline_cols)} columns)\n")
    print(f"Total Columns: {len(baseline_cols)}")
    print(f"Full Header List: {baseline_cols}\n")
    
    print(f"--- Comparison Report ---")

    for i in range(1, len(files)):
        current_file = files[i]
        current_cols = set(headers_dict[current_file])
        
        added = current_cols - baseline_cols
        removed = baseline_cols - current_cols
        
        print(f"File: {current_file} ({len(current_cols)})")
        
        if not added and not removed:
            print("  - Result: Headers match perfectly.")
        else:
            if added:
                print(f"  - Extra columns (New): {added}")
            if removed:
                print(f"  - Missing columns (Removed): {removed}")
        print("-" * 30)

if os.path.exists(folder):
    headers = get_stata_headers(stata_files, folder)
    compare_headers(headers)
else:
    print(f"Directory '{folder}' not found. Please ensure the folder exists in your current path.")
