import pandas as pd

csmar_fund_allocation = pd.read_csv('data/CSMAR/Fund_Allocation.csv', parse_dates=['EndDate'])
csmar_fund_allocation = csmar_fund_allocation.rename(columns={'EndDate': 'Date'})
csmar_fund_allocation['Date'] = csmar_fund_allocation.Date.dt.to_period('M')