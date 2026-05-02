import pandas as pd
import config

df_excel = pd.read_excel('Filtered_All_countries_SDC_2015-2024.xlsx')
excel_false_ipo = set(df_excel[df_excel['Original IPO Flag'].astype(str).str.upper() == "FALSE"]['Datastream'].dropna().astype(str))

df_stata = pd.read_stata(config.STATA_INPUT)
stata_dscds = set(df_stata['dscd'].dropna().astype(str))

found_in_stata = excel_false_ipo.intersection(stata_dscds)
missing_in_stata = excel_false_ipo - stata_dscds

print(f"Excel (FALSE IPO) 總數: {len(excel_false_ipo)}")
print(f"在 Stata 中找到的個數: {len(found_in_stata)}")
print(f"具體重複的 dscd: {found_in_stata}")
print(f"缺失的個數: {len(missing_in_stata)}")