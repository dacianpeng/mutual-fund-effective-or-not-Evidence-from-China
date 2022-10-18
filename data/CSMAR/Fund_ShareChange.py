import pandas as pd

csmar_share_info = pd.read_csv('data/CSMAR/Fund_ShareChange.csv', parse_dates=['EndDate'])
csmar_share_info = csmar_share_info.rename(columns={'EndDate': 'Date'})
csmar_share_info['Date'] = csmar_share_info.Date.dt.to_period('M')
csmar_share_info['Symbol'] = csmar_share_info.Symbol.astype(str).str.zfill(6)