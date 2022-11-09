
import pandas as pd
import numpy as np
from scipy.stats import zscore
from functools import reduce
from IPython.display import display

import datetime
import matplotlib.pyplot as plt

from factors import *
from data.SVC.svc_source import svc_source
from data.CSMAR.FUND_PurchRedChg import tradable
from data.TwoStepData.csmar_blend_fund_weight_yearly import csmar_blend_fund_weight_yearly
from data.TwoStepData.csmar_stock_fund_weight_yearly import csmar_stock_fund_weight_yearly
from data.TwoStepData.return_of_csmar_blend_fund import return_of_csmar_blend_fund
from data.TwoStepData.return_of_csmar_stock_fund import return_of_csmar_stock_fund
from data.TwoStepData.filtered_funds import filtered_funds
from utils.my_cache import cache_wrapper
from utils.functions import *


def select_funds(z_scored_all_factors, top_num : int):
    return z_scored_all_factors.apply(lambda x: x.nlargest(top_num).index, axis=1)

def get_selected_fund_return(date_funds, weighting='1/n'):
    
    date = date_funds.name
    funds = date_funds.values[0]

    if weighting == '1/n':
        return return_of_all_fund_.shift(-1).loc[date, funds].mean()

    elif weighting == 'mkt':
        weights = all_fund_weight.loc[date, funds]
        weights /= weights.sum()

        return (return_of_all_fund_.shift(-1).loc[date, funds] * weights).sum()


@cache_wrapper(expire = 60 * 60 * 24 * 30)
def test_factors(all_factors, start_time = '2005-6', end_time = datetime.datetime.today().strftime('%Y-%m-%d'),\
     truncate_proportion = .01, MIN_VALID_NUM = 15, ivol_truncate = .2, mkt_truncate = .2, return_truncate = .01, mdd_month = 6, es_proportion = .05):

    '''
    all_factors : list of dicts

    start_time : str
    
    factor test start time

    end_time : str
    
    factor test end time

    truncate_proportion :  float

    handle extreme values in factors

    MIN_VALID_NUM : int

    set NA if fund's one factor do not meet the min valid data requirement

    ivol_truncate : float
    
    handle extreme volatility in funds

    mkt_truncate : float

    handle small market value funds

    return_truncate : float

    handle wrong return data (mainly caused by wrong fund division month)

    mdd_month : int

    rolling month for maximum draw down
    
    es_proportion : float

    the tail proportion for expected shortfall

    '''



    concatenated_all_factors = pd.concat(list(map(lambda x: x.loc[start_time: end_time], all_factors.values())))

    concatenated_all_factors = concatenated_all_factors.apply(lambda x: \
        x.dropna()[np.logical_and(x.dropna() > x.dropna().quantile(truncate_proportion), x.dropna() < x.dropna().quantile(1 - truncate_proportion))], \
            axis=1)
    ivol_condition = return_of_all_fund_.rolling(12).std()
    ivol_condition = pd.notna(ivol_condition.apply(lambda x: x.dropna()[np.logical_and(x.dropna() > x.dropna().quantile(ivol_truncate), x.dropna() < x.dropna().quantile(1 - ivol_truncate))], axis=1))
    ivol_condition = ivol_condition.stack()[ivol_condition.stack()].index

    mkt_value_condition = pd.notna(all_fund_weight.apply(lambda x: x.dropna()[x.dropna() > x.dropna().quantile(mkt_truncate)], axis=1))
    mkt_value_condition = mkt_value_condition.stack()[mkt_value_condition.stack()].index

    filtered_funds_condition = filtered_funds.stack()[filtered_funds.stack()].index

    z_scored_all_factors = concatenated_all_factors.apply(lambda x: zscore(x.dropna())\
            if pd.notna(x).sum() >= MIN_VALID_NUM else pd.Series([np.nan] * len(x), index=x.index), axis=1)

    return_condition = pd.notna(return_of_all_fund_.apply(lambda x: x.dropna()[np.logical_and(x.dropna() > x.dropna().quantile(return_truncate), x.dropna() < x.dropna().quantile(1 - return_truncate))], axis=1))
    return_condition = return_condition.stack()[return_condition.stack()].index

    filtered_index = reduce(lambda x, y: np.intersect1d(x, y), \
        [ivol_condition, mkt_value_condition, filtered_funds_condition, return_condition, z_scored_all_factors.stack().index])

    z_scored_all_factors = z_scored_all_factors.stack().loc[filtered_index].groupby(level=[0,1]).mean()

    assume_tradable_part = z_scored_all_factors.loc[: tradable.index[0] - pd.offsets.MonthEnd(1)]
    assume_not_tradable_part = z_scored_all_factors.loc[tradable.index[0]: ]
    co_funds = np.intersect1d(tradable.columns, assume_not_tradable_part.unstack().columns)
    tradable_ = tradable[co_funds]
    assume_not_tradable_part = assume_not_tradable_part.loc[np.intersect1d(assume_not_tradable_part.index, tradable_.stack().index)]
    z_scored_all_factors = pd.concat([assume_tradable_part, assume_not_tradable_part]).unstack()

    selected_funds = select_funds(z_scored_all_factors, 10)
    funds_return = pd.DataFrame(selected_funds).apply(lambda x: get_selected_fund_return(x, 'mkt'), axis=1)
    funds_return.index = funds_return.index + pd.offsets.MonthEnd(1)

    plot_start_time = funds_return.index[0]

    mkt_return = svc_source.loc[plot_start_time: ].mktrf + svc_source.loc[plot_start_time: ].rf
    
    statistics = []

    for top_num in [1, 3 ,5 ,10]:
        selected_funds = select_funds(z_scored_all_factors, top_num)
        funds_return = pd.DataFrame(selected_funds).apply(lambda x: get_selected_fund_return(x, 'mkt'), axis=1)
        funds_return.index = funds_return.index + pd.offsets.MonthEnd(1)

        co_index = np.intersect1d(funds_return.index, mkt_return.index)
        regression = sm.OLS(funds_return.loc[co_index], sm.add_constant(mkt_return).loc[co_index]).fit().params
        α = regression.iloc[0]
        annual_α = (α + 1) ** 12 - 1
        β = regression.iloc[1]
        annual_return = (funds_return + 1).cumprod().iloc[-1] ** (1 / ((funds_return.index[-1] - funds_return.index[0]).n / 12)) - 1
        excess_return = funds_return.loc[co_index] - svc_source.loc[plot_start_time: ].rf.loc[co_index]
        excess_annual_return = (excess_return + 1).cumprod().iloc[-1] ** (1 / ((excess_return.index[-1] - excess_return.index[0]).n / 12)) - 1
        sharpe = excess_return.mean() / excess_return.std()
        mdd = (funds_return + 1).cumprod().rolling(mdd_month).apply(lambda x: (x[-1] - x.max())/x[-1]).replace([np.inf, -np.inf], np.nan).dropna().min()
        es_proportional = funds_return.sort_values()[: int(es_proportion * len(funds_return))].mean()
        win_rate = (funds_return.loc[co_index] > mkt_return.loc[co_index]).sum() / len(co_index)

        statistics.append([sharpe, β, f'{(α * 100).round(2)}%', f'{(annual_α * 100).round(2)}%', f'{(mdd * 100).round(2)}%',
            f'{(win_rate * 100).round(2)}%', f'{(es_proportional * 100).round(2)}%', f'{(annual_return * 100).round(2)}%', f'{(excess_annual_return * 100).round(2)}%'])

        plt.yscale('log', base=2)
        (funds_return + 1).cumprod().plot(figsize=(24, 8), label=f'top {top_num} funds')

    columns = ['monthly sharpe', 'β', 'monthly α', 'annual α', f'{mdd_month} month MDD', 'win rate', f'{int(es_proportion * 100)}% ES', 'compounded annual return', 'excess compounded annual return']

    table = pd.DataFrame(statistics, index=[f'top {num} fund(s)' for num in [1, 3 ,5 ,10]], columns=columns)

    display(table)

    ((return_of_csmar_stock_fund.unstack().T.dropna(how='all').sort_index() * csmar_stock_fund_weight_yearly.sort_index()).sum(axis=1) + 1).loc[plot_start_time:].cumprod().plot(label='Stock Fund Cumulative Return')
    ((return_of_csmar_blend_fund.unstack().T.dropna(how='all').sort_index() * csmar_blend_fund_weight_yearly.sort_index()).sum(axis=1) + 1).loc[plot_start_time:].cumprod().plot(label='Blend Fund Cumulative Return')
    ((svc_source.loc[plot_start_time: ].mktrf + svc_source.loc[plot_start_time: ].rf) + 1).cumprod().plot(label='Market Portfolio Cumulative Return')

    plt.grid()
    plt.legend()
    plt.show()

    return selected_funds
