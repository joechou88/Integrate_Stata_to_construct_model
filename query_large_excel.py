import pandas as pd
import numpy as np
import config

print(f"Loading datasets:\n  - {config.SECURITY_PRICE_INPUT}")
df = pd.read_csv(config.SECURITY_PRICE_INPUT)

filtered_df = df[df['sedol'] == '5165294'] 
print(filtered_df)