import pandas as pd
import config

sdc_df = pd.read_excel(config.SDC_INPUT)

sdc_df['dscd'] = sdc_df['Datastream'].astype(str).str.strip().replace(['nan', 'None', ''], None)
sdc_df['year'] = sdc_df['Dates: Offer Year (CCYY)'].astype(int)

counts = sdc_df[sdc_df['dscd'].notna()].groupby(['dscd', 'year']).size().reset_index(name='count')
duplicate_summary = counts[counts['count'] > 1].sort_values(['count', 'dscd'], ascending=[False, True])

output_file = "SDC_Datastream_duplicates_list.txt"
with open(output_file, "w", encoding="utf-8") as f:
    f.write("SDC Datastream+Year 重複清單\n")
    f.write("="*50 + "\n")
    f.write(f"總計重複行數: {len(duplicate_summary)}\n\n")
    
    if len(duplicate_summary) > 0:
        f.write(duplicate_summary.to_string(index=False))
    else:
        f.write("未發現重複筆數。")

print(f"重複清單已成功輸出至: {output_file}")
print(f"清單中包含 {len(duplicate_summary)} 筆重複記錄。")
