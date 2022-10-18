import dask.dataframe as ddf
import pandas as pd

csmar_stock_index_weight = ddf.read_csv('data/CSMAR/index_weight/*', dtype={'Indexcd': 'object'}).compute()
csmar_stock_index_weight['Enddt'] = pd.to_datetime(csmar_stock_index_weight.Enddt)

csmar_sz50_weight = csmar_stock_index_weight[csmar_stock_index_weight.Indexcd == '000016'].pivot(index=['Enddt'], columns='Stkcd', values='Weight')
csmar_sz50_weight = csmar_sz50_weight.resample('M').last().to_period('M')

csmar_hs300_weight = csmar_stock_index_weight[csmar_stock_index_weight.Indexcd == '000300'].pivot(index=['Enddt'], columns='Stkcd', values='Weight')
csmar_hs300_weight = csmar_hs300_weight.resample('M').last().to_period('M')

csmar_zz500_weight = csmar_stock_index_weight[csmar_stock_index_weight.Indexcd == '000905'].pivot(index=['Enddt'], columns='Stkcd', values='Weight')
csmar_zz500_weight = csmar_zz500_weight.resample('M').last().to_period('M')