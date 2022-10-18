import pandas as pd
import numpy as np


wind_validate_stock_fund_adj_nav = pd.read_excel('data/Wind/wind_validate_stock_fund_adj_nav.xlsx')
wind_validate_stock_fund_adj_nav.columns = np.concatenate([wind_validate_stock_fund_adj_nav.columns[:2].values, wind_validate_stock_fund_adj_nav.columns[2:].str[-17:-7]])
wind_validate_stock_fund_adj_nav.index = wind_validate_stock_fund_adj_nav.iloc[:, 0].str[:-3]
wind_validate_stock_fund_adj_nav = wind_validate_stock_fund_adj_nav.iloc[:, 2:]
wind_validate_stock_fund_adj_nav.columns = pd.to_datetime(wind_validate_stock_fund_adj_nav.columns).to_period('M')
wind_validate_stock_fund_adj_nav = wind_validate_stock_fund_adj_nav.T.sort_index()
wind_validate_stock_fund_adj_nav.index.name = 'Date'
wind_validate_stock_fund_adj_nav.columns.name = ''