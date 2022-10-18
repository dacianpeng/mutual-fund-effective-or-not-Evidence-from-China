import os
import sys
import pandas as pd
import jqdatasdk as jq

from data.JoinQuant.jq_all_stocks_brief import jq_all_stocks_brief

sys.path.append(os.getcwd())
from utils.my_cache import cache_wrapper


@cache_wrapper(expire = 60 * 60 * 24 * 7)
def jq_industry(all_stocks):
    jq_stock_classification = jq.get_industry(list(all_stocks.index), date=None)
    return jq_stock_classification

jq_stock_classification = jq_industry(jq_all_stocks_brief)
jq_stock_classification = pd.DataFrame(jq_stock_classification).loc['sw_l1'].dropna().apply(lambda info: info['industry_name'])
jq_stock_classification = pd.DataFrame([jq_stock_classification.index.str.split('.').str[0], jq_stock_classification.values], index=['Stkcd', 'Indnme']).T
jq_stock_classification['Stkcd'] = jq_stock_classification.Stkcd.astype(int)