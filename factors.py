
import numpy as np
import pandas as pd

import statsmodels.api as sm

from utils.functions import *

from data.TwoStepData.return_of_all_fund import return_of_all_fund
from data.TwoStepData.all_fund_weight import all_fund_weight
from data.TwoStepData.regression_source import regression_source
from data.TwoStepData.main_data import main_data

return_of_all_fund_ = return_of_all_fund.unstack(0)


def group_and_statistic(α_matrix, groups = 5, weighting = 'mkt', interval = 1):
    '''
    weighting : string

    mkt, market value weighted

    1/n, equal weighted

    interval : int

    the frequency to change holdings
    '''

    α_matrix = α_matrix.resample(f'{interval}M').ffill().dropna(how='all', axis=0).iloc[: -1]
    α_matrix.index = α_matrix.index.astype(np.datetime64).to_period('M')

    grouped_all_fund_α_matrix = α_matrix.apply(lambda x: \
        pd.qcut(x, groups, labels=np.arange(groups)) if pd.notna(x).sum() >= groups else pd.Series([np.nan] * len(x), x.index), axis=1).dropna(how='all')

    adj_NAV = main_data.adj_NAV.unstack().T
    return_look_forward = adj_NAV.pct_change(1).shift(-1)

    def func(x):
        date = x.name
        weight = all_fund_weight.loc[date]
        ret = return_look_forward.loc[date]
        result = pd.DataFrame([x, ret, weight], index=['rank', 'ret', 'weight']).T.dropna().set_index('rank', append=True).swaplevel().sort_index()

        if weighting == 'mkt':
            result['weight'] = result.groupby(level=0).apply(lambda y: y.weight / y.weight.sum()).values
        elif weighting == '1/n':
            result['weight'] = [groups / len(result.index.levels[1])] * len(result.index.levels[1])

        result = result.groupby(level=0).apply(lambda y: (y.ret * y.weight).sum())
        return result

    grouped_all_fund_α_matrix_return = grouped_all_fund_α_matrix.resample('M').ffill().apply(lambda x: func(x), axis=1)

    RS_α = pd.merge(grouped_all_fund_α_matrix_return, regression_source, on='Date')
    RS_α[['stock_fund', 'mktrf', 'rf', 'smb', 'vmg', 'blend_fund']] = RS_α[['stock_fund', 'mktrf', 'rf', 'smb', 'vmg', 'blend_fund']].shift(-1)
    RS_α = RS_α.iloc[:-1].interpolate()

    regressors = [
        ['α'],
        ['α', 'mktrf'],
        ['α', 'mktrf', 'smb', 'vmg']
        ]
        
    results = []

    for regressor in regressors:

        for group in range(groups):
            temp = sm.OLS(RS_α[group] - RS_α.rf, RS_α[regressor]).fit()
            monthly_α = temp.params[0]
            # monthly_α = ((α + 1) ** (1 / interval)) - 1
            results.append([float_to_percent(monthly_α), yearly_return(monthly_α), temp.tvalues[0].round(3), temp.rsquared.round(3), int(temp.nobs)])
        # remove r_f
        temp = sm.OLS(RS_α[groups - 1] - RS_α[0], RS_α[regressor]).fit()
        monthly_α = temp.params[0]
        # monthly_α = ((α + 1) ** (1 / interval)) - 1
        results.append([float_to_percent(monthly_α), yearly_return(monthly_α), temp.tvalues[0].round(3), temp.rsquared.round(3), int(temp.nobs)])

    excess_result, capm_α_result, svc_α_result = results[0: groups + 1], results[groups + 1: 2 * groups + 2], results[2 * groups + 2: 3 * groups + 3]

    excess_result = pd.DataFrame(np.array(excess_result).T, \
        index=pd.MultiIndex.from_product([['excess'], ['α (monthly)', 'annual α', 't', 'R^2', 'Obs']]), columns=['group' + str(i) for i in range(groups)] + ['long-short'])
    capm_α_result = pd.DataFrame(np.array(capm_α_result).T, \
        index=pd.MultiIndex.from_product([['capm α'], ['α (monthly)', 'annual α', 't', 'R^2', 'Obs']]), columns=['group' + str(i) for i in range(groups)] + ['long-short'])
    svc_α_result = pd.DataFrame(np.array(svc_α_result).T, \
        index=pd.MultiIndex.from_product([['svc α'], ['α (monthly)', 'annual α', 't', 'R^2', 'Obs']]), columns=['group' + str(i) for i in range(groups)] + ['long-short'])

    return pd.concat([excess_result, capm_α_result, svc_α_result])



def fund_ended_check(α_operation):
    def check_filter(x):
        if pd.notna(x[-1]):
            # if the fund is running now
            return α_operation(x)
        else:
            # if the fund is shut down
            return np.nan
    return check_filter


@fund_ended_check
def α_na_ratio(x):

    window_length = len(x)
    x = x.dropna()  
    return 1 - len(x) / window_length


MAX_NA_NUM = 35

# return_of_all_fund_na_ratio = return_of_all_fund_.rolling(window = 36, min_periods = 36 - MAX_NA_NUM).apply(α_na_ratio)

