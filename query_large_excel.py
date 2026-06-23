import duckdb
import config

query = f"SELECT * FROM '{config.SECURITY_PRICE_INPUT}' WHERE sedol = '5165294'"
filtered_df = duckdb.query(query).to_df()
print(filtered_df)

output_filename = "global_security_daily_price_2014_2024_5165294.csv"
filtered_df.to_csv(output_filename, index=False)
print(f"Exported to: {output_filename}")
