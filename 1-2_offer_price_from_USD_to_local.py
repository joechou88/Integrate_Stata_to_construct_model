import pandas as pd
import config

print(f"Loading datasets:\n  - {config.EXCHANGE_RATE_2015_2024}\n  - {config.COUNTRY_CODE_WITH_CURD}\n  - {config.SDC_OUTPUT}")
exchange_rate_df = pd.read_csv(config.EXCHANGE_RATE_2015_2024)
curd_df = pd.read_excel(config.COUNTRY_CODE_WITH_CURD)
stata_df = pd.read_stata(config.SDC_OUTPUT)

stata_df['Issue_Date'] = pd.to_datetime(stata_df['Issue_Date'])
exchange_rate_df['datadate'] = pd.to_datetime(exchange_rate_df['datadate'])

stata_df = pd.merge(
    stata_df,
    curd_df[['Country_code2', 'curd']],
    left_on='country_code2',
    right_on='Country_code2',
    how='left'
)
stata_df = pd.merge(
    stata_df,
    exchange_rate_df[['datadate', 'curd', 'exratd_fromusd']],
    left_on=['Issue_Date', 'curd'],
    right_on=['datadate', 'curd'],
    how='left'
)

stata_df['Offer_Price_Local'] = stata_df['Offer_Price_USD'] * stata_df['exratd_fromusd']

stata_df = stata_df.drop(columns=['Country_code2', 'curd', 'datadate', 'curd', 'exratd_fromusd'])
stata_df['Issue_Date'] = stata_df['Issue_Date'].dt.strftime('%Y-%m-%d')

output_path = config.OFFER_PRICE_OUTPUT
stata_df.to_stata(output_path, write_index=False)
print(f"Exported to: {output_path}\n")