from factors import *
from IPython.display import display

@fund_ended_check
def svc_α_generation(x):
    x = x.dropna()  
    temp_dates = x.index
    temp_regression = regression_source.loc[temp_dates]
    α = sm.OLS(x - temp_regression.rf, temp_regression[['α', 'mktrf', 'smb', 'vmg']]).fit().params[0]
    return α

all_fund_svc_α = return_of_all_fund_.loc['2005-6': '2019-6'].rolling(window = 36, min_periods = 36 - MAX_NA_NUM).apply(svc_α_generation)

display(group_and_statistic(all_fund_svc_α))