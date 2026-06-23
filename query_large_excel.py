import duckdb
import config

sedol = "BTPJH25"
query = f"SELECT * FROM '{config.SECURITY_PRICE_INPUT}' WHERE sedol = '{sedol}'"
filtered_df = duckdb.query(query).to_df()
print(filtered_df)

output_filename = f"{sedol}_global_security_daily_price_2014_2024.csv"
filtered_df.to_csv(output_filename, index=False)
print(f"Exported to: {output_filename}")
