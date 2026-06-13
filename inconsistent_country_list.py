import pandas as pd
import config

sdc_df = pd.read_excel(config.SDC_INPUT)
stata_df = pd.read_stata(config.OPERATING_LEASE_NPV_INPUT).copy()

sdc_df['year'] = sdc_df['Dates: Offer Year (CCYY)'].astype(int)
stata_df['year'] = stata_df['year'].astype(int)

sdc_df = sdc_df[['Issuer/Borrower SEDOL', 'year', 'Country']].rename(
    columns={'Issuer/Borrower SEDOL': 'sedol', 'Country': 'SDC_country'}
)
stata_df = stata_df[['sedol', 'year', 'country']].rename(
    columns={'country': 'Worldscope_country'}
)

comparison_df = pd.merge(
    sdc_df, 
    stata_df, 
    on=['sedol', 'year'], 
    how='left'
)

sdc_country = comparison_df['SDC_country'].astype(str).str.lower().str.replace(r'[\W_]+', '', regex=True)
ws_country = comparison_df['Worldscope_country'].astype(str).str.lower().str.replace(r'[\W_]+', '', regex=True)

country_aliases = {
    'uk': 'unitedkingdom'
}

sdc_country = sdc_country.replace(country_aliases)
ws_country = ws_country.replace(country_aliases)

mismatches = comparison_df[sdc_country != ws_country].copy()
mismatches.columns = ['sedol', 'year','SDC_country', 'Worldscope_country']

mismatches.to_csv('SDC_Worldscope_country_mismatches.csv', index=False)
print("Exported to SDC_Worldscope_country_mismatches.csv successfully.")