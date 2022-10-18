import pandas as pd

amac_full_market_value = pd.read_csv('data/AMAC/amac.csv', sep='\t', index_col=0).astype(float)
amac_full_market_value.index = pd.to_datetime(amac_full_market_value.index.astype(str)) + pd.Timedelta('180 days')