
import numpy as np

from data.CSMAR.invest_detail import invest_detail
from data.TwoStepData.filtered_funds import filtered_funds

invest_detail['Symbol'] = invest_detail.Symbol.astype(float)
filtered_funds.columns = filtered_funds.columns.astype(float)
co_index = np.intersect1d(invest_detail.set_index(['Date', 'Symbol']).index, filtered_funds.stack()[filtered_funds.stack()].index)

invest_detail = invest_detail.set_index(['Date', 'Symbol']).loc[co_index]
invest_detail = invest_detail.reset_index()
invest_detail['Symbol'] = invest_detail.Symbol.astype(int).astype(str)

invest_detail.to_pickle(open('data/TwoStepData/invest_detail.pkl', 'wb'))