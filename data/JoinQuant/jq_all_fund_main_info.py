from data.JoinQuant.jq_all_fund_brief import *
from utils.my_cache import cache_wrapper
import math
import os
import sys

import jqdatasdk as jq
import numpy as np
import pandas as pd

sys.path.append(os.getcwd())


jq.auth('13764432461', 'Swisschina6')


@cache_wrapper(expire=60 * 60 * 24 * 7)
def main_info(fund_codes) -> pd.DataFrame:
    limit = jq.DBTable.RESULT_ROWS_LIMIT
    fund_code_cuts = np.array_split(
        fund_codes, math.ceil(len(fund_codes) / limit))
    full_table_cuts = []
    for code_cut in fund_code_cuts:
        table_cut = jq.finance.run_query(jq.query(jq.finance.FUND_MAIN_INFO).filter(
            jq.finance.FUND_MAIN_INFO.main_code.in_(code_cut)))
        full_table_cuts.append(table_cut)
    full_table = pd.concat(full_table_cuts).reset_index(drop=True)
    full_table['start_date'] = full_table.start_date.astype(
        np.datetime64).dt.to_period('M')
    return full_table


jq_all_fund_main_info = main_info(jq_all_fund_code)[
    ['main_code', 'underlying_asset_type', 'operate_mode', 'start_date']]
