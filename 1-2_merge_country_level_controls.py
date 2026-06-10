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

control_columns = [
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

for key in primary_keys:
    if key not in excel_raw.columns:
        raise ValueError(f"Excel 中找不到欄位 '{key}'，現有欄位：{list(excel_raw.columns)}")

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

hk_2020_economic_freedom = control_df.loc[(control_df['country_code'] == 'HK') & (control_df['year'] == 2020), 'Economic_Freedom']
if not hk_2020_economic_freedom.empty:
    score_val = hk_2020_economic_freedom.values[0]
    hk_later_mask = (control_df['country_code'] == 'HK') & (control_df['year'].isin([2021, 2022, 2023, 2024]))
    control_df.loc[hk_later_mask, 'Economic_Freedom'] = score_val
    print(f"  [INFO] 已將香港 (HK) 2020 年的 Economic_Freedom 分數 ({score_val}) 填入 2021-2024 年，並保留其他變數原始值。")

print(f"\nLoading {config.SDC_OUTPUT}")
stata_df = pd.read_stata(config.SDC_OUTPUT)
stata_df['country_code'] = stata_df['country_code'].astype(str).str.strip()
stata_df['year'] = pd.to_numeric(stata_df['year'], errors='coerce')
total_obs = len(stata_df)
print(f"  Stata rows      : {total_obs}")

overlap_columns = [c for c in control_columns if c in stata_df.columns]
if overlap_columns:
    print(f"\n  [WARN] Stata 中已有以下欄位，將以 Excel 值覆蓋：{overlap_columns}")
    stata_df = stata_df.drop(columns=overlap_columns)

print("\n執行 left-join 合併 ...")
control_df['year'] = control_df['year']
merged_df = pd.merge(stata_df, control_df, on=primary_keys, how='left')

matched = merged_df[control_columns[0]].notna().sum()
unmatched = merged_df[control_columns[0]].isna().sum()
print(f"  合併後總行數  : {len(merged_df)}")
print(f"  成功匹配筆數  : {matched} / {total_obs}")
print(f"  未匹配筆數    : {unmatched} / {total_obs}")

if unmatched > 0:
    unmatched_df = merged_df[merged_df[control_columns[0]].isna()]
    missing_summary = unmatched_df.groupby(['country_code', 'year']).size().reset_index(name='counts')
    
    missing_txt_path = "1-2_missing_country_controls_for_country_year_combinations.txt"
    missing_summary.to_csv(missing_txt_path, sep='\t', index=False)
    print(f"  [INFO] 已將未匹配的清單（共 {len(missing_summary)} 筆組合）存至 {missing_txt_path}")
    merged_df = merged_df.dropna(subset=[control_columns[0]])
    print(f"  [INFO] 已將 {unmatched} 筆未匹配資料從合併結果中剔除。")
else:
    print("  [INFO] 所有資料皆完美匹配，未產生 missing 清單。")

if len(merged_df) > total_obs:
    raise RuntimeError(
        f"合併後行數 ({len(merged_df)}) 不等於原始行數 ({total_obs})，"
        "請檢查 Excel 是否有非唯一的 [country_code + year] 組合。"
    )

output_path = config.COUNTRY_LEVEL_CONTROLS_OUTPUT
merged_df.to_stata(output_path, write_index=False)

print(f"\n[OK] 完成！成功寫出 {len(merged_df)} 筆資料至 {output_path}")
print("=" * 60)