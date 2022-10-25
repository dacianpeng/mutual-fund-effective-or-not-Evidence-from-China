import pandas as pd

csmar_monthly_stock = pd.read_csv('data/CSMAR/TRD_Mnth.csv')
csmar_monthly_stock['Date'] = pd.to_datetime(csmar_monthly_stock.Trdmnt).dt.to_period('M')
csmar_monthly_stock = csmar_monthly_stock.drop(columns='Trdmnt')