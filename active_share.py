import numpy as np

from IPython.display import display
from data.CSMAR.index_weight import *
from data.CSMAR.invest_detail import invest_detail
from data.JoinQuant.jq_stock_classification import jq_stock_classification
from data.TwoStepData.return_of_all_fund import return_of_all_fund
from factors import *


return_of_all_fund_ = (return_of_all_fund.unstack(0) - 1).loc['2005-6': '2019-6']

invest_detail_ = pd.merge(invest_detail, jq_stock_classification[['Stkcd', 'Indnme']], on='Stkcd', validate='m:1')
invest_detail_ = invest_detail_.rename(columns={'EndDate': 'Date'})
invest_detail_['Date'] = pd.to_datetime(invest_detail_.Date).dt.to_period('M')

invest_detail_ = invest_detail_.drop_duplicates(['Symbol', 'Date', 'Stkcd'])

invest_detail_ = invest_detail_[invest_detail_.Date >= '2005-6']

invest_detail_ = invest_detail_.pivot(index=['Symbol', 'Date'], columns='Stkcd', values='Proportion')

invest_detail_ = invest_detail_.div(invest_detail_.sum(axis=1), axis=0) * 100


hs300_weight_in_csmar_form = pd.DataFrame(columns=csmar_hs300_weight.columns, index=invest_detail_.index, \
    data=pd.merge(csmar_hs300_weight, pd.Series(invest_detail_.index.get_level_values(1).values, name='Enddt'), on='Enddt', how='right').iloc[:, 1:].values)

hs300_co_stocks = np.intersect1d(invest_detail_.columns, hs300_weight_in_csmar_form.columns)
hs300_AS = (np.abs(hs300_weight_in_csmar_form[hs300_co_stocks] - invest_detail_[hs300_co_stocks])).sum(axis=1) / 2

sz50_weight_in_csmar_form = pd.DataFrame(columns=csmar_sz50_weight.columns, index=invest_detail_.index, \
    data=pd.merge(csmar_sz50_weight, pd.Series(invest_detail_.index.get_level_values(1).values, name='Enddt'), on='Enddt', how='right').iloc[:, 1:].values)

sz50_co_stocks = np.intersect1d(invest_detail_.columns, csmar_sz50_weight.columns)
sz50_AS = (np.abs(sz50_weight_in_csmar_form[sz50_co_stocks] - invest_detail_[sz50_co_stocks])).sum(axis=1) / 2

zz500_weight_in_csmar_form = pd.DataFrame(columns=csmar_zz500_weight.columns, index=invest_detail_.index, \
    data=pd.merge(csmar_zz500_weight, pd.Series(invest_detail_.index.get_level_values(1).values, name='Enddt'), on='Enddt', how='right').iloc[:, 1:].values)

zz500_co_stocks = np.intersect1d(invest_detail_.columns, csmar_zz500_weight.columns)
zz500_AS = (np.abs(zz500_weight_in_csmar_form[zz500_co_stocks] - invest_detail_[zz500_co_stocks])).sum(axis=1) / 2

active_share = pd.concat([hs300_AS, zz500_AS, sz50_AS], axis=1).replace(0, np.inf).min(axis=1).unstack(0)

co_funds = np.intersect1d(active_share.columns, return_of_all_fund_.columns)

active_share = active_share[co_funds].replace(np.inf, np.nan).ffill().loc['2005-6' : '2019-6']

display(group_and_statistic(active_share))