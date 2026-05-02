import pandas as pd
import config

sdc_df = pd.read_excel(config.SDC_INPUT)
stata_df = pd.read_stata(config.STATA_INPUT)

id_column_mapping = {
    'dscd': 'Datastream',
    'isin': 'ISIN',
    'sedol': 'Issuer/Borrower SEDOL',
}

for stata_col, sdc_col in id_column_mapping.items():
    stata_df[stata_col] = stata_df[stata_col].astype(str).str.strip().replace(['nan', 'None', ''], None)
    sdc_df[stata_col] = sdc_df[sdc_col].astype(str).str.strip().replace(['nan', 'None', ''], None)

stata_df['year'] = stata_df['year'].astype(int)
sdc_df['year'] = sdc_df['Dates: Offer Year (CCYY)'].astype(int)

stata_duplicates = stata_df.duplicated(subset=['dscd', 'year']).sum()
print(f"Stata 中 ID+Year 重複的行數: {stata_duplicates}")

sdc_duplicates = sdc_df.duplicated(subset=['dscd', 'year']).sum()
print(f"SDC 中 ID+Year 重複的行數: {sdc_duplicates}")