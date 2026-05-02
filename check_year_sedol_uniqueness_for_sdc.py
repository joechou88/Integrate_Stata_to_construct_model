import pandas as pd
import config

sdc_df = pd.read_excel(config.SDC_INPUT)

sdc_df['sedol'] = sdc_df['Issuer/Borrower SEDOL'].astype(str).str.strip().replace(['nan', 'None', ''], None)
sdc_df['year'] = sdc_df['Dates: Offer Year (CCYY)'].astype(int)

duplicates = sdc_df[sdc_df.duplicated(subset=['sedol', 'year'], keep=False)]
duplicates_sorted = duplicates.sort_values(['sedol', 'year'])

output_file = "SDC_SEDOL_duplicates_list.txt"
with open(output_file, "w", encoding="utf-8") as f:
    f.write("SDC SEDOL + Year 重複清單\n")
    f.write("="*50 + "\n")
    f.write(f"總計重複行數: {len(duplicates_sorted)}\n\n")
    
    if len(duplicates_sorted) > 0:
        f.write(duplicates_sorted.to_string(index=False))
    else:
        f.write("未發現重複筆數。")

print(f"重複清單已成功輸出至: {output_file}")
print(f"清單中包含 {len(duplicates_sorted)} 筆重複記錄。")
