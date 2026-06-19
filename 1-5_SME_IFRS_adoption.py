import pandas as pd
import config

print(f"Loading datasets:\n  - {config.SME_INPUT}\n  - {config.INST_OUTPUT}")
sme_df = pd.read_excel(config.SME_INPUT)
stata_df = pd.read_stata(config.INST_OUTPUT)

sme_df = sme_df[["Country_code2", "SME_IFRS_adoption"]]
merged_df = pd.merge(stata_df, sme_df, left_on="country_code2", right_on="Country_code2", how="left")
merged_df = merged_df.drop(columns=["Country_code2"])

output_path = config.SME_OUTPUT
merged_df.to_stata(output_path, write_index=False)
print(f"Exported to: {output_path}\n")
