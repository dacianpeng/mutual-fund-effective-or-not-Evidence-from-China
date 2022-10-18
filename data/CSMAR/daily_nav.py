import dask.dataframe as ddf
import pandas as pd

csmar_nav_daily = ddf.read_csv('data/CSMAR/daily_nav/*').compute()
csmar_nav_daily = csmar_nav_daily.rename(columns={'TradingDate': 'Date'})
csmar_nav_daily['Date'] = pd.to_datetime(csmar_nav_daily.Date)