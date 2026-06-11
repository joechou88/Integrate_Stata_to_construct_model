import pandas as pd
import os
import config

input_files = [
    # config.MARKET_PRICE_INPUT,
    # config.SECURITY_PRICE_INPUT,
    config.WORLDSCOPE_FUNDAMENTALS_INPUT
]

for input_file in input_files:
    base_name = os.path.basename(input_file)
    original_name = os.path.splitext(base_name)[0]
    output_file = f'head_1000_{original_name}.csv'

    df = pd.read_csv(input_file, nrows=1000)
    df.to_csv(output_file, index=False)

    print(f"Saved head 1000 data in: {output_file}")