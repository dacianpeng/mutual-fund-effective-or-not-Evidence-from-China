import dask.dataframe as ddf
import pandas as pd
from data.CSMAR.FUND_FundCodeInfo import csmar_symbol_code_mapping

csmar_invest_detail = ddf.read_csv('data/CSMAR/invest_detail/*', low_memory=False, dtype={'Symbol': 'object'}).compute()
csmar_invest_detail = csmar_invest_detail.rename(columns={'Symbol': 'Stkcd'})

def aboard_stock(x):
    try:
        int(x)
        return False
    except:
        return True

# 1.8% aboard_stock dropped
aboard_stock_filter = csmar_invest_detail.Stkcd.apply(aboard_stock)
invest_detail = csmar_invest_detail[~ aboard_stock_filter]
invest_detail = pd.merge(invest_detail, csmar_symbol_code_mapping.groupby('MasterFundCode').last(), on='MasterFundCode', how='left', validate='m:1')
invest_detail['Stkcd'] = invest_detail.Stkcd.astype(int)
invest_detail = invest_detail[['Symbol', 'EndDate', 'Stkcd', 'Proportion']].groupby(['Symbol', 'EndDate', 'Stkcd']).last().reset_index()