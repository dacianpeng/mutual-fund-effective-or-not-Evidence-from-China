import pandas as pd
csmar_maininfo = pd.read_csv('data/CSMAR/FUND_MainInfo.csv', parse_dates=['InceptionDate'])
csmar_maininfo['InceptionDate'] = csmar_maininfo.InceptionDate.dt.to_period('M')