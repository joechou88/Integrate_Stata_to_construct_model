import pandas as pd
import config

print(f"Loading datasets:\n  - {config.WORLDSCOPE_EQUITY_COUNTS_OUTPUT}")
stata_df = pd.read_stata(config.WORLDSCOPE_EQUITY_COUNTS_OUTPUT)

start_year = 2015
end_year = 2022
stata_df = stata_df[stata_df['year'].between(start_year, end_year)]

stata_df.rename(columns={'Ln_GDPOP': 'Ln_GDP_per_capita_US'}, inplace=True)
stata_df['sic1digit'] = stata_df['sic1'].dropna().astype(int).astype(str).str.zfill(4).str[0].astype(int)

ordered_columns = [
    "sedol",
    "isin",
    "dscd",
    "year",
    "country",
    "country_code2",
    "sic1",
    "sic1digit",
    "sic2digit",
    "Underpricing",
    "Post",
    "lease_intensity_pre",
    "high_lease", 
    "SME_IFRS_adoption",
    "Age",
    "Ln_Age",
    "bign",
    "sales_lag",
    "ln_sales_lag",
    "capex_at_lag",
    "rd_at_lag",
    "roa_ebitda_lag",
    "lev_lag",
    "INST",
    "Relative_Offer_Size",
    "VC_backed",
    "Firm_Commitment",
    "Underwriter_Reputation",
    "Bookbuilt",
    "Market_Return",
    "Ln_Market_Return",
    "Market_Volatility",
    "IPO_Activities",
    "Ln_IPO_Activities",
    "Price_Stabilization",
    "Economic_Freedom",
    "CAP_Ratio",
    "Ln_CAP_Ratio",
    "GDP_per_capita_US",
    "Ln_GDP_per_capita_US",
    "GDP_per_capita_growth",
    "AFOL"
]

missing_cols = [col for col in ordered_columns if col not in stata_df.columns]
if missing_cols:
    print(f"[Warning] The following columns were not found in the dataset and will be skipped: {missing_cols}")

valid_columns = [col for col in ordered_columns if col in stata_df.columns]
stata_df = stata_df[valid_columns].copy()

total_rows = len(stata_df)
missing_counts = stata_df.isnull().sum()
print("Missing value proportions per column:")
for col, missing_count in missing_counts.items():
    print(f"  - {col:<18}: {missing_count}/{total_rows} missing")

print(f"\n--- Sample Selection Steps ---")
print(f"Initial total samples: {total_rows}")
selection_df = stata_df.copy()

# 1. Worldscope data
previous_sample_count = len(selection_df)
selection_df = selection_df.dropna(subset=["bign"])
print(f"Unable to match Worldscope data: Dropped {previous_sample_count - len(selection_df)} | Remaining: {len(selection_df)}")

# 2. Underpricing
previous_sample_count = len(selection_df)
selection_df = selection_df.dropna(subset=["Underpricing"])
print(f"Missing value for Underpricing variable: Dropped {previous_sample_count - len(selection_df)} | Remaining: {len(selection_df)}")

# 3. lease
previous_sample_count = len(selection_df)
selection_df = selection_df.dropna(subset=["lease_intensity_pre", "high_lease"])
print(f"Missing value for high_lease variable: Dropped {previous_sample_count - len(selection_df)} | Remaining: {len(selection_df)}")

# 4. INST
previous_sample_count = len(selection_df)
selection_df = selection_df.dropna(subset=["INST"])
print(f"Missing value for INST variable: Dropped {previous_sample_count - len(selection_df)} | Remaining: {len(selection_df)}")

# 5. Age
previous_sample_count = len(selection_df)
selection_df = selection_df.dropna(subset=["Ln_Age"])
print(f"Missing value for Age variable: Dropped {previous_sample_count - len(selection_df)} | Remaining: {len(selection_df)}")

# 6. Other firm characteristics
previous_sample_count = len(selection_df)
selection_df = selection_df.dropna(subset=["ln_sales_lag", "capex_at_lag", "rd_at_lag", "roa_ebitda_lag", "lev_lag"])
print(f"Missing value for other firm characteristics controls: Dropped {previous_sample_count - len(selection_df)} | Remaining: {len(selection_df)}")

# 7. Deal characteristics
previous_sample_count = len(selection_df)
selection_df = selection_df.dropna(subset=["Relative_Offer_Size", "VC_backed", "Firm_Commitment", "Underwriter_Reputation", "Bookbuilt"])
print(f"Missing value for deal characteristics controls: Dropped {previous_sample_count - len(selection_df)} | Remaining: {len(selection_df)}")

# 8. Country-level controls
previous_sample_count = len(selection_df)
selection_df = selection_df.dropna(subset=["Ln_Market_Return", "Market_Volatility", "Ln_IPO_Activities", "Price_Stabilization", "Economic_Freedom", "Ln_CAP_Ratio", "Ln_GDP_per_capita_US", "GDP_per_capita_growth"])
print(f"Missing value for country-level controls: Dropped {previous_sample_count - len(selection_df)} | Remaining: {len(selection_df)}")

# 9. Drop any remaining missing values (from base variables not explicitly listed above)
previous_sample_count = len(selection_df)
selection_df = selection_df.dropna()
if previous_sample_count != len(selection_df):
    print(f"Missing value for remaining unlisted base variables: Dropped {previous_sample_count - len(selection_df)} | Remaining: {len(selection_df)}")

remaining_sample_count = len(selection_df)
print(f"\nFinal remaining samples after dropping all rows with missing values: {remaining_sample_count}")

output_path = f"Stata/IPO_{start_year}_{end_year}_filtered.dta"
stata_df.to_stata(output_path, write_index=False)
print(f"Exported to: {output_path}\n")
