
import os
import sys
import time

import jqdatasdk as jq
import pandas as pd

sys.path.append(os.getcwd())

from utils.my_cache import cache_wrapper

jq.auth('13764432461', 'Swisschina6')

@cache_wrapper(expire = 60 * 60 * 24 * 7)
# cache to avoid unnecessary traffic
def brief_of_funds() -> pd.DataFrame:
    return jq.get_all_securities(['fund', 'open_fund'], time.strftime('%Y%m%d'))


jq_all_fund_brief = brief_of_funds()
jq_all_fund_code = jq_all_fund_brief.index.str.split('.').str[0]
