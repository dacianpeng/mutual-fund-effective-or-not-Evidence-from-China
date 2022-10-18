import pandas as pd


csmar_symbol_code_mapping = pd.read_csv('data/CSMAR/FUND_FundCodeInfo.csv')
csmar_symbol_code_mapping = csmar_symbol_code_mapping[['MasterFundCode', 'Symbol']].drop_duplicates()
csmar_symbol_code_mapping['Symbol'] = csmar_symbol_code_mapping.Symbol.astype(str).str.zfill(6)