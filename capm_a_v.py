from factors import *
from IPython.display import display

@fund_ended_check
def capm_α_ε_generation(x):
    x = x.dropna()  
    temp_dates = x.index
    temp_regression = regression_source.loc[temp_dates]
    result = sm.OLS(x - temp_regression.rf, temp_regression[['α', 'mktrf']]).fit()
    α = result.params[0]
    ε = result.resid.std()
    division = α / ε

    if division < 1e3 and division > 1e-3:
        return division
    else:
        return np.nan

all_fund_capm_α_ε = return_of_all_fund_.loc['2005-6': '2019-6'].rolling(window = 36, min_periods = 36 - MAX_NA_NUM).apply(capm_α_ε_generation)

display(group_and_statistic(all_fund_capm_α_ε))