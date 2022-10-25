
import pickle
import numpy as np
import pandas as pd
from data.CSMAR.Fund_ShareChange import csmar_share_info
from data.JoinQuant.jq_all_fund_main_info import jq_all_fund_main_info
from data.TwoStepData.main_data_raw import main_data
from data.TwoStepData.csmar_nav_monthly import csmar_nav_monthly

from utils.functions import *

main_data['NAV_shift'] = main_data.groupby(level=0).apply(lambda x: x.NAV.shift(1)).droplevel(0)
main_data['adj_factor'] = main_data.groupby(level=0).apply(lambda x: (x.SplitRatio * x.NAV_shift / (x.NAV_shift - x.DividendperShare)).cumprod()).droplevel(0)
main_data['adj_NAV'] = main_data.NAV * main_data.adj_factor

blend_data = main_data[main_data.underlying_asset_type == '混合型']
stock_data = main_data[main_data.underlying_asset_type == '股票型']

return_of_csmar_stock_fund = stock_data.adj_NAV.groupby(level=0).apply(lambda x: x.pct_change())
return_of_csmar_stock_fund.name = 'return_of_csmar_stock_fund'
return_of_csmar_blend_fund = blend_data.adj_NAV.groupby(level=0).apply(lambda x: x.pct_change())
return_of_csmar_blend_fund.name = 'return_of_csmar_blend_fund'
return_of_all_fund = main_data.adj_NAV.groupby(level=0).apply(lambda x: x.pct_change())
return_of_all_fund.name = 'return_of_all_fund'

MONTH_OF_YEAR = 6

csmar_share_info = csmar_share_info.drop_duplicates(subset=['Symbol', 'Date']).pivot(index='Date', columns='Symbol', values='EndDateShares')

csmar_share_info_yearly = csmar_share_info[csmar_share_info.index.month == MONTH_OF_YEAR]
csmar_nav_yearly = csmar_nav_monthly[csmar_nav_monthly.index.month == MONTH_OF_YEAR]

csmar_co_time_6 = np.intersect1d(csmar_share_info_yearly.index, csmar_nav_yearly.index)

csmar_blend_code_6 = np.intersect1d(csmar_nav_yearly.columns, jq_all_fund_main_info[jq_all_fund_main_info.underlying_asset_type == '混合型'].main_code.values)
csmar_blend_code_6 = np.intersect1d(csmar_blend_code_6, csmar_share_info_yearly.columns)

csmar_stock_code_6 = np.intersect1d(csmar_nav_yearly.columns, jq_all_fund_main_info[jq_all_fund_main_info.underlying_asset_type == '股票型'].main_code.values)
csmar_stock_code_6 = np.intersect1d(csmar_stock_code_6, csmar_share_info_yearly.columns)



csmar_stock_fund_weight_yearly = (csmar_share_info_yearly.loc[csmar_co_time_6, csmar_stock_code_6] * csmar_nav_yearly.loc[csmar_co_time_6, csmar_stock_code_6])

csmar_stock_fund_weight_yearly = pd.concat([csmar_stock_fund_weight_yearly, \
    pd.DataFrame([[np.nan] * csmar_stock_fund_weight_yearly.shape[1]], index=[pd.to_datetime('2023-06').to_period('M')], columns=csmar_stock_fund_weight_yearly.columns)])

csmar_stock_fund_weight_yearly = csmar_stock_fund_weight_yearly.resample('M').ffill()

stock_fund_dates = return_of_csmar_stock_fund.unstack(level=0).index
stock_fund_funds = return_of_csmar_stock_fund.unstack(level=0).columns

stock_fund_new = np.setdiff1d(stock_fund_funds, csmar_stock_fund_weight_yearly.columns)
print(f'{stock_fund_new} will not be used')

stock_fund_funds = np.intersect1d(stock_fund_funds, csmar_stock_fund_weight_yearly.columns)

csmar_stock_fund_weight_yearly = csmar_stock_fund_weight_yearly.loc[stock_fund_dates, stock_fund_funds]
csmar_stock_fund_weight_yearly = csmar_stock_fund_weight_yearly.div(csmar_stock_fund_weight_yearly.sum(axis=1), axis=0)


csmar_blend_fund_weight_yearly = (csmar_share_info_yearly.loc[csmar_co_time_6, csmar_blend_code_6] * csmar_nav_yearly.loc[csmar_co_time_6, csmar_blend_code_6])
csmar_blend_fund_weight_yearly = pd.concat([csmar_blend_fund_weight_yearly, \
    pd.DataFrame([[np.nan] * csmar_blend_fund_weight_yearly.shape[1]], index=[pd.to_datetime('2023-06').to_period('M')], columns=csmar_blend_fund_weight_yearly.columns)])
csmar_blend_fund_weight_yearly = csmar_blend_fund_weight_yearly.resample('M').ffill()

blend_fund_dates = return_of_csmar_blend_fund.unstack(level=0).index
blend_fund_funds = return_of_csmar_blend_fund.unstack(level=0).columns

blend_fund_new = np.setdiff1d(blend_fund_funds, csmar_blend_fund_weight_yearly.columns)
print(f'{blend_fund_new} will not be used')
blend_fund_funds = np.intersect1d(blend_fund_funds, csmar_blend_fund_weight_yearly.columns)

csmar_blend_fund_weight_yearly = csmar_blend_fund_weight_yearly.loc[blend_fund_dates, blend_fund_funds]
csmar_blend_fund_weight_yearly = csmar_blend_fund_weight_yearly.div(csmar_blend_fund_weight_yearly.sum(axis=1), axis=0)


pickle.dump(csmar_share_info_yearly, open('data/TwoStepData/csmar_share_info_yearly.pkl', 'wb'))
pickle.dump(csmar_nav_yearly, open('data/TwoStepData/csmar_nav_yearly.pkl', 'wb'))
pickle.dump(csmar_stock_fund_weight_yearly, open('data/TwoStepData/csmar_stock_fund_weight_yearly.pkl', 'wb'))
pickle.dump(csmar_blend_fund_weight_yearly, open('data/TwoStepData/csmar_blend_fund_weight_yearly.pkl', 'wb'))
pickle.dump(main_data, open('data/TwoStepData/main_data.pkl', 'wb'))
pickle.dump(return_of_csmar_stock_fund, open('data/TwoStepData/return_of_csmar_stock_fund.pkl', 'wb'))
pickle.dump(return_of_csmar_blend_fund, open('data/TwoStepData/return_of_csmar_blend_fund.pkl', 'wb'))
pickle.dump(return_of_all_fund, open('data/TwoStepData/return_of_all_fund.pkl', 'wb'))


all_fund_weight = csmar_share_info_yearly * csmar_nav_yearly
all_fund_weight = pd.concat([all_fund_weight, \
    pd.DataFrame([[np.nan] * all_fund_weight.shape[1]], index=[pd.to_datetime('2023-06').to_period('M')], columns=all_fund_weight.columns)])
all_fund_weight = all_fund_weight.resample('M').ffill()

pickle.dump(all_fund_weight, open('data/TwoStepData/all_fund_weight.pkl', 'wb'))

