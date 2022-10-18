import pandas as pd

csmar_fund_resolution = pd.read_csv('data/CSMAR/Fund_Resolution.csv', parse_dates=['DeclareDate'])
csmar_fund_resolution['Symbol'] = csmar_fund_resolution.Symbol.astype(str).str.zfill(6)
csmar_fund_resolution = csmar_fund_resolution.rename(columns={'DeclareDate': 'Date'})
csmar_fund_resolution['SplitRatio'] = csmar_fund_resolution.SplitRatio.fillna(1)
csmar_fund_resolution['Date'] = csmar_fund_resolution.Date.dt.to_period('M')
csmar_fund_resolution = pd.DataFrame(csmar_fund_resolution.groupby(['Symbol', 'Date']).prod().to_records())