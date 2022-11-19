
import pickle
import datetime
from functools import reduce

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
from IPython.display import display
from scipy.stats import zscore

from data.CSMAR.FUND_PurchRedChg import tradable
from data.CSMAR.TRD_Mnth import csmar_monthly_stock
from data.SVC.svc_source import svc_source
from data.TwoStepData.csmar_blend_fund_weight_yearly import \
    csmar_blend_fund_weight_yearly
from data.TwoStepData.csmar_stock_fund_weight_yearly import \
    csmar_stock_fund_weight_yearly
from data.TwoStepData.filtered_funds import filtered_funds
from data.TwoStepData.invest_detail import invest_detail
from data.TwoStepData.return_of_all_fund import return_of_all_fund
from data.TwoStepData.return_of_csmar_blend_fund import \
    return_of_csmar_blend_fund
from data.TwoStepData.return_of_csmar_stock_fund import \
    return_of_csmar_stock_fund
from data.Wind.wind_stock_classification import wind_stock_classification
from factors import *
from utils.functions import *
from utils.my_cache import cache_wrapper
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


start_time = '2005-6'
end_time = datetime.datetime.now().strftime('%Y-%m')
return_of_all_fund_ = return_of_all_fund.unstack(0).loc[start_time: end_time]

invest_detail_ = pd.merge(invest_detail, wind_stock_classification[[
                          'Stkcd', 'Indnme']], on='Stkcd', validate='m:1')

month_mkt_value_ = pd.merge(
    csmar_monthly_stock, wind_stock_classification, on='Stkcd', validate='m:1')
month_mkt_value_ = month_mkt_value_.groupby(
    ['Date', 'Indnme']).apply(lambda x: x.Msmvttl.sum())
month_mkt_value_ = month_mkt_value_.unstack().div(
    month_mkt_value_.unstack().sum(axis=1), axis=0).fillna(0)

invest_industry_sum = invest_detail_.groupby(
    ['Symbol', 'Date', 'Indnme']).apply(lambda x: x.Proportion.sum())
invest_industry_proportion = invest_industry_sum / \
    invest_industry_sum.groupby(level=[0, 1]).sum()
unstacked = invest_industry_proportion.unstack(level=[0, 2]).T
all_quarters = pd.date_range(
    '2000-1', datetime.datetime.now().strftime('%Y-%m'), freq='q').to_period('M')
invest_industry_proportion = invest_industry_sum / \
    invest_industry_sum.groupby(level=[0, 1]).sum()
unstacked = invest_industry_proportion.unstack(level=[0, 2]).T
unstacked.loc[:, unstacked.columns.isin(
    all_quarters)] = unstacked.loc[:, unstacked.columns.isin(all_quarters)].fillna(0)
unstacked[(datetime.datetime.now() + pd.offsets.QuarterEnd(0) -
           pd.offsets.MonthEnd(1)).strftime('%Y-%m')] = np.nan
unstacked = unstacked.T
invest_industry_proportion = unstacked.resample(
    'M').ffill().fillna(method='ffill')
invest_industry_proportion = invest_industry_proportion.stack(
    0).swaplevel().sort_index().fillna(0)

month_mkt_value_ = pd.merge(invest_industry_proportion.reset_index()[['Symbol', 'Date']], month_mkt_value_, on='Date')\
    .set_index(['Symbol', 'Date']).sort_index()

invest_industry_proportion.index = invest_industry_proportion.index.set_levels(
    invest_industry_proportion.index.levels[0].str.zfill(6), level=0)

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


# @cache_wrapper(expire = 60 * 60 * 24 * 30)
def test_factors(all_factors, start_time='2005-6', end_time=datetime.datetime.today().strftime('%Y-%m-%d'),
                 truncate_proportion=.01, MIN_VALID_NUM=15, ivol_truncate=.2, mkt_truncate=.2, return_truncate=.01, mdd_month=6, es_proportion=.05):
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

    concatenated_all_factors = pd.concat(
        list(map(lambda x: x.loc[start_time: end_time], all_factors.values())))

    concatenated_all_factors = concatenated_all_factors.apply(lambda x:
                                                              x.dropna()[np.logical_and(x.dropna() > x.dropna().quantile(
                                                                  truncate_proportion), x.dropna() < x.dropna().quantile(1 - truncate_proportion))],
                                                              axis=1)
    ivol_condition = return_of_all_fund_.rolling(12).std()
    ivol_condition = pd.notna(ivol_condition.apply(lambda x: x.dropna()[np.logical_and(x.dropna(
    ) > x.dropna().quantile(ivol_truncate), x.dropna() < x.dropna().quantile(1 - ivol_truncate))], axis=1))
    ivol_condition = ivol_condition.stack()[ivol_condition.stack()].index
    mkt_value_condition_ = all_fund_weight > 1e7
    mkt_value_condition_ = mkt_value_condition_.stack(
    )[mkt_value_condition_.stack()].index
    mkt_value_condition = pd.notna(all_fund_weight.apply(
        lambda x: x.dropna()[x.dropna() > x.dropna().quantile(mkt_truncate)], axis=1))
    mkt_value_condition = mkt_value_condition.stack(
    )[mkt_value_condition.stack()].index

    filtered_funds_condition = filtered_funds.stack()[
        filtered_funds.stack()].index

    z_scored_all_factors = concatenated_all_factors.apply(lambda x: zscore(x.dropna())
                                                          if pd.notna(x).sum() >= MIN_VALID_NUM else pd.Series([np.nan] * len(x), index=x.index), axis=1)

    return_condition = pd.notna(return_of_all_fund_.apply(lambda x: x.dropna()[np.logical_and(x.dropna(
    ) > x.dropna().quantile(return_truncate), x.dropna() < x.dropna().quantile(1 - return_truncate))], axis=1))
    return_condition = return_condition.stack()[return_condition.stack()].index

    filtered_index = reduce(lambda x, y: np.intersect1d(x, y),
                            [ivol_condition, mkt_value_condition, mkt_value_condition_, filtered_funds_condition, return_condition, z_scored_all_factors.stack().index])

    z_scored_all_factors = z_scored_all_factors.stack(
    ).loc[filtered_index].groupby(level=[0, 1]).mean()

    assume_tradable_part = z_scored_all_factors.loc[:
                                                    tradable.index[0] - pd.offsets.MonthEnd(1)]
    assume_not_tradable_part = z_scored_all_factors.loc[tradable.index[0]:]
    co_funds = np.intersect1d(
        tradable.columns, assume_not_tradable_part.unstack().columns)
    tradable_ = tradable[co_funds]
    assume_not_tradable_part = assume_not_tradable_part.loc[np.intersect1d(
        assume_not_tradable_part.index, tradable_.stack().index)]
    z_scored_all_factors = pd.concat(
        [assume_tradable_part, assume_not_tradable_part]).unstack()

    selected_funds = select_funds(z_scored_all_factors, 10)
    funds_return = pd.DataFrame(selected_funds).apply(
        lambda x: get_selected_fund_return(x, '1/n'), axis=1)
    funds_return.index = funds_return.index + pd.offsets.MonthEnd(1)

    plot_start_time = funds_return.index[0]

    mkt_return = svc_source.loc[plot_start_time:].mktrf + \
        svc_source.loc[plot_start_time:].rf
    fig, axes = plt.subplots(2, 1, figsize=(24, 16))

    statistics = []

    columns = ['monthly sharpe', 'annual sharpe', 'monthly std', 'annual std', 'β', 'monthly α', 'annual α', f'{mdd_month} month MDD', 'win rate',
               f'{int(es_proportion * 100)}% ES', 'compounded annual return', 'excess compounded annual return', 'last month', 'last 3 months', 'last 6 months',
               'cumulative all', 'past year', 'past 3 year p.a.', 'past 5 year p.a.', 'past 10 year p.a.']
    fig1_plot_data = {}
    fig2_plot_data = {}
    for top_num in ['沪深300', 3, 5, 10]:
        if top_num != '沪深300':
            selected_funds = select_funds(z_scored_all_factors, top_num)

            selected_funds.to_excel(f'result/{top_num}/selected_funds.xlsx')

            indexes = []
            for date in selected_funds.index:
                indexes.append(
                    list(zip([date] * len(selected_funds), selected_funds.loc[date])))

            indexes = pd.MultiIndex.from_tuples(
                list(map(lambda x: tuple(x), np.array(indexes).reshape(-1, 2))))
            co_indexes = np.intersect1d(
                invest_industry_proportion.swaplevel().index, indexes)
            selected_funds_allocation = invest_industry_proportion.swaplevel(
            ).loc[co_indexes]
            co_indexes = np.intersect1d(selected_funds_allocation.index,
                                        csmar_stock_fund_weight_yearly.stack().index)
            selected_funds_allocation.loc[co_indexes].multiply(
                csmar_stock_fund_weight_yearly.stack().loc[co_indexes], axis=0)
            selected_funds_allocation = selected_funds_allocation.groupby(
                level=0).sum().resample('y').sum()
            selected_funds_allocation = selected_funds_allocation.div(
                selected_funds_allocation.sum(axis=1), axis=0)
            selected_funds_allocation.to_excel(
                f'result/{top_num}/selected_funds_allocation.xlsx')

            funds_return = pd.DataFrame(selected_funds).apply(
                lambda x: get_selected_fund_return(x, 'mkt'), axis=1)
            funds_return.index = funds_return.index + pd.offsets.MonthEnd(1)
            funds_return.to_excel(f'result/{top_num}/funds_return.xlsx')

        elif top_num == '沪深300':
            funds_return = svc_source.loc[plot_start_time:].hs300

        co_index = np.intersect1d(funds_return.index, mkt_return.index)
        regression = sm.OLS(funds_return.loc[co_index], sm.add_constant(
            mkt_return).loc[co_index]).fit().params
        α = regression.iloc[0]
        annual_α = (α + 1) ** 12 - 1
        β = regression.iloc[1]
        annual_return = (funds_return + 1).cumprod().iloc[-1] ** (
            1 / ((funds_return.index[-1] - funds_return.index[0]).n / 12)) - 1
        excess_return = funds_return.loc[co_index] - \
            svc_source.loc[plot_start_time:].rf.loc[co_index]
        excess_annual_return = (excess_return + 1).cumprod().iloc[-1] ** (
            1 / ((excess_return.index[-1] - excess_return.index[0]).n / 12)) - 1
        sharpe = excess_return.mean() / excess_return.std()
        # excess_return_ = excess_return.resample('y').apply(lambda x: (1 + x).cumprod()[-1] - 1)
        annual_sharpe = np.sqrt(12) * sharpe
        mdd = (funds_return + 1).cumprod().rolling(mdd_month).apply(lambda x: (
            x[-1] - x.max())/x[-1]).replace([np.inf, -np.inf], np.nan).dropna().min()
        monthly_std = funds_return.std()
        annual_std = np.sqrt(12) * funds_return.std()
        es_proportional = funds_return.sort_values()[: int(
            es_proportion * len(funds_return))].mean()
        win_rate = (funds_return.loc[co_index] >
                    mkt_return.loc[co_index]).sum() / len(co_index)
        last_month = funds_return.loc[(
            datetime.datetime.now() - pd.offsets.MonthEnd(1)).to_period('M')]
        last_3_month = ((funds_return.loc[(datetime.datetime.now() - pd.offsets.MonthEnd(3)).to_period('M'): (
            datetime.datetime.now() - pd.offsets.MonthEnd(1)).to_period('M')] + 1).cumprod() - 1).iloc[-1]
        last_6_month = ((funds_return.loc[(datetime.datetime.now() - pd.offsets.MonthEnd(6)).to_period('M'): (
            datetime.datetime.now() - pd.offsets.MonthEnd(1)).to_period('M')] + 1).cumprod() - 1).iloc[-1]
        cumulative_all = (funds_return + 1).cumprod().iloc[-1]
        #
        past_year = ((funds_return.loc[(datetime.datetime.now() - pd.offsets.MonthEnd(12)).to_period('M'): (
            datetime.datetime.now() - pd.offsets.MonthEnd(1)).to_period('M')] + 1).cumprod() - 1).iloc[-1]
        past_3_year = ((funds_return.loc[(datetime.datetime.now() - pd.offsets.MonthEnd(36)).to_period('M'): (
            datetime.datetime.now() - pd.offsets.MonthEnd(1)).to_period('M')] + 1).cumprod() - 1).iloc[-1]
        annual_past_3_year = ((past_3_year + 1) ** (1 / 3)) - 1
        past_5_year = ((funds_return.loc[(datetime.datetime.now() - pd.offsets.MonthEnd(60)).to_period('M'): (
            datetime.datetime.now() - pd.offsets.MonthEnd(1)).to_period('M')] + 1).cumprod() - 1).iloc[-1]
        annual_past_5_year = ((past_5_year + 1) ** (1 / 5)) - 1
        past_10_year = ((funds_return.loc[(datetime.datetime.now() - pd.offsets.MonthEnd(120)).to_period('M'): (
            datetime.datetime.now() - pd.offsets.MonthEnd(1)).to_period('M')] + 1).cumprod() - 1).iloc[-1]
        annual_past_10_year = ((past_10_year + 1) ** (1 / 10)) - 1

        statistics.append([sharpe, annual_sharpe, monthly_std, annual_std, β, α, annual_α, mdd,
                           win_rate, es_proportional, annual_return, excess_annual_return,
                           last_month, last_3_month, last_6_month, cumulative_all, past_year,
                           annual_past_3_year, annual_past_5_year, annual_past_10_year])

        pd.DataFrame(statistics).to_excel(
            f'result/{top_num}/statistics.xlsx')

        if top_num != '沪深300':

            ax1 = axes[0]
            ax1.set_yscale('log', base=2)
            cumulative_return = (funds_return + 1).cumprod()

            cumulative_return.to_excel(
                f'result/{top_num}/cumulative_return.xlsx')

            cumulative_return.plot(label=f'Top {top_num}', ax=axes[0])
            fig1_plot_data[f'Top {top_num}'] = cumulative_return

        per_year_return = funds_return.resample('y').apply(
            lambda x: (x + 1).cumprod().iloc[-1] - 1)
        per_year_return.to_excel(f'result/{top_num}/per_year_return.xlsx')

        ax2 = axes[1]
        if top_num != '沪深300':
            ax2.bar(per_year_return.index.to_timestamp() - pd.offsets.MonthEnd(6) + pd.offsets.MonthEnd(2 * len(statistics)),
                    per_year_return.values * 100, width=50, label=f'Top {top_num}')
            fig2_plot_data[f'Top {top_num}'] = per_year_return
        else:
            ax2.bar(per_year_return.index.to_timestamp() - pd.offsets.MonthEnd(6) + pd.offsets.MonthEnd(2 * len(statistics)),
                    per_year_return.values * 100, width=50, label='沪深300')
            fig2_plot_data['沪深300'] = per_year_return

    table = pd.DataFrame(statistics, index=[
                         '沪深300'] + [f'Top {top_num}' for top_num in [3, 5, 10]], columns=columns)
    difference = table.iloc[1:] - table.iloc[0]
    difference.index = [f'{top_num} 超额' for top_num in [3, 5, 10]]
    table = pd.concat([table, difference])
    table[columns[5:]] = (table[columns[5:]] * 100).round(2).astype(str) + '%'
    table = table.reindex(
        ['沪深300', 'Top 3', '3 超额', 'Top 5', '5 超额', 'Top 10', '10 超额'])
    display(table)
    table.to_excel('result/table.xlsx')

    ((return_of_csmar_stock_fund.unstack().T.dropna(how='all').sort_index() * csmar_stock_fund_weight_yearly.sort_index()
      ).sum(axis=1) + 1).loc[plot_start_time:].cumprod().plot(label='股票型基金累计收益', ax=axes[0])
    ((return_of_csmar_blend_fund.unstack().T.dropna(how='all').sort_index() * csmar_blend_fund_weight_yearly.sort_index()
      ).sum(axis=1) + 1).loc[plot_start_time:].cumprod().plot(label='混合型基金累计收益', ax=axes[0])
    (svc_source.loc[plot_start_time:].hs300 +
        1).cumprod().plot(label='沪深300累计收益', ax=axes[0])
    fig1_plot_data['股票型基金'] = ((return_of_csmar_stock_fund.unstack().T.dropna(how='all').sort_index() * csmar_stock_fund_weight_yearly.sort_index()
                                ).sum(axis=1) + 1).loc[plot_start_time:].cumprod()
    fig1_plot_data['混合型基金'] = ((return_of_csmar_blend_fund.unstack().T.dropna(how='all').sort_index() * csmar_blend_fund_weight_yearly.sort_index()
                                ).sum(axis=1) + 1).loc[plot_start_time:].cumprod()
    fig1_plot_data['沪深300'] = (
        svc_source.hs300 + 1).loc[plot_start_time:].cumprod()

    fig1 = pd.concat(fig1_plot_data, axis=1)
    fig1.index = fig1.index.astype(str)
    fig2 = pd.concat(fig2_plot_data, axis=1)
    fig2.index = fig2.index.astype(str)
    fig1.to_excel('result/fig1.xlsx')
    fig2.to_excel('result/fig2.xlsx')

    ax1.grid()
    ax2.grid(axis='y')
    ax1.legend()
    ax1.set_title('累计收益')
    ax2.legend()
    ax2.yaxis.set_major_formatter(ticker.PercentFormatter())
    ax2.set_title('当年收益')
    plt.savefig('result/demo.png', transparent=True)
    plt.show()

    return selected_funds
