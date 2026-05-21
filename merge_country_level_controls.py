import pandas as pd
import config

print("=" * 60)
print("讀取 Excel country controls ...")
excel_raw = pd.read_excel(config.COUNTRY_LEVEL_CONTROLS_INPUT)
excel_raw.columns = [c.replace(" ", "_") for c in excel_raw.columns]
excel_raw = excel_raw.rename(columns={
    'Country_code': 'country_code', 
    'Year': 'year',
    'Overall_Score': 'Economic_Freedom'
})
primary_keys = ["country_code", "year"]
start_column = 12
end_column = 13

for key in primary_keys:
    if key not in excel_raw.columns:
        raise ValueError(f"Excel 中找不到欄位 '{key}'，現有欄位：{list(excel_raw.columns)}")

control_columns = list(excel_raw.columns[start_column:end_column])
for col in control_columns:
    excel_raw[col] = pd.to_numeric(excel_raw[col], errors='coerce')
control_df = excel_raw[primary_keys + control_columns].copy()

print(f"  Excel rows      : {len(control_df)}")
print(f"  Control columns : {control_columns}")
print(f"  Primary keys    : {primary_keys}")

control_df['country_code'] = control_df['country_code'].astype(str).str.strip()
control_df['year'] = pd.to_numeric(control_df['year'], errors='coerce')

duplicate_mask = control_df.duplicated(subset=primary_keys, keep='first')
if duplicate_mask.any():
    print(f"  [WARN] Excel 中有重複的 Key 組合，將保留第一筆。")
    control_df = control_df.drop_duplicates(subset=primary_keys, keep='first')

print("\n讀取 Stata .dta ...")
stata_df = pd.read_stata(config.STATA_SDC_OUTPUT)
# 確保 Stata 欄位格式一致
stata_df['country_code'] = stata_df['country_code'].astype(str).str.strip()
stata_df['year'] = pd.to_numeric(stata_df['year'], errors='coerce')
total_obs = len(stata_df)
print(f"  Stata rows      : {total_obs}")

overlap_columns = [c for c in control_columns if c in stata_df.columns]
if overlap_columns:
    print(f"\n  [WARN] Stata 中已有以下欄位，將以 Excel 值覆蓋：{overlap_columns}")
    stata_df = stata_df.drop(columns=overlap_columns)

print("\n執行 left-join 合併 ...")
control_df['year'] = control_df['year'] + 1     # t 對 t-1 併，以避免前視偏誤 (Look-ahead bias)
merged_df = pd.merge(stata_df, control_df, on=primary_keys, how='left')

matched = merged_df[control_columns[0]].notna().sum()
unmatched = merged_df[control_columns[0]].isna().sum()
print(f"  合併後總行數  : {len(merged_df)}")
print(f"  成功匹配筆數  : {matched} / {total_obs}")
print(f"  未匹配筆數    : {unmatched} / {total_obs}")

if len(merged_df) != total_obs:
    raise RuntimeError(
        f"合併後行數 ({len(merged_df)}) 不等於原始行數 ({total_obs})，"
        "請檢查 Excel 是否有非唯一的 [country_code + year] 組合。"
    )

cols_to_move = [
    'Economic_Freedom', 
    'GDP_per_capita_US', 
    'Ln_GDPOP', 
    'GDP_per_capita_growth', 
    'Land_area', 
    'Listed_domestic_companies', 
    'Ln_Listed', 
    'CAP_Ratio', 
    'str'
]

current_cols = merged_df.columns.tolist()
valid_cols_to_move = []
for c in cols_to_move:
    if c in current_cols:
        current_cols.remove(c)
        valid_cols_to_move.append(c)
    else:
        print(f"  [WARN] 找不到指定的調整欄位: {c}")

insert_index = min(123, len(current_cols))
new_col_order = current_cols[:insert_index] + valid_cols_to_move + current_cols[insert_index:]

merged_df = merged_df[new_col_order]
print(f"\n  [INFO] 已將 Economic_Freedom 等 {len(valid_cols_to_move)} 個欄位移動至 Index={insert_index} 的位置。")

output_path = config.STATA_COUNTRY_LEVEL_CONTROLS_OUTPUT
merged_df.to_stata(output_path, write_index=False)

print(f"\n[OK] 完成！成功寫出 {len(merged_df)} 筆資料至 {output_path}")
print("=" * 60)