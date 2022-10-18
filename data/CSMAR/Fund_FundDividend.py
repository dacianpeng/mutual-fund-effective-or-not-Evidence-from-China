import pandas as pd

csmar_fund_dividend = pd.read_csv('data/CSMAR/Fund_FundDividend.csv', parse_dates=['PrimaryExDividendDate', 'SecondaryExDividendDate'])
csmar_fund_dividend['Symbol'] = csmar_fund_dividend.Symbol.astype(str).str.zfill(6)
ExDividendMonth = csmar_fund_dividend.PrimaryExDividendDate.copy()
ExDividendMonth.name = 'ExDividendMonth'
ExDividendMonth[ExDividendMonth.isnull()] = csmar_fund_dividend.SecondaryExDividendDate[ExDividendMonth.isnull()].copy()
csmar_fund_dividend['ExDividendMonth'] = ExDividendMonth
csmar_fund_dividend = csmar_fund_dividend[['Symbol', 'ExDividendMonth', 'DividendperShare']]
csmar_fund_dividend = csmar_fund_dividend.rename(columns={'ExDividendMonth': 'Date'})
csmar_fund_dividend['DividendperShare'] = csmar_fund_dividend.DividendperShare.fillna(0)
csmar_fund_dividend['Date'] = csmar_fund_dividend.Date.dt.to_period('M')
csmar_fund_dividend = pd.DataFrame(csmar_fund_dividend.groupby(['Symbol', 'Date']).sum().to_records())