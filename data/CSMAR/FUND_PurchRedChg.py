from data.TwoStepData.filtered_funds import filtered_funds
import pandas as pd
import numpy as np


pur_red = pd.read_csv('data/CSMAR/FUND_PurchRedChg.csv')
pur_red['Symbol'] = pur_red.Symbol.astype(str).str.zfill(6)
pur_red['ChangeDate'] = pd.to_datetime(pur_red.ChangeDate).dt.to_period('M')
co_index = np.intersect1d(pd.MultiIndex.from_frame(pur_red[['ChangeDate', 'Symbol']]), filtered_funds.stack()[filtered_funds.stack()].index)
pur_red = pur_red.set_index(['ChangeDate', 'Symbol']).loc[co_index].reset_index()
unlock_same_month = pur_red[pur_red.duplicated(subset=['ChangeDate', 'Symbol', 'PurchaseStatus'])].copy()
unlock_same_month['PurchaseStatus'] = False
def unlock_same_month(x):

    if len(x) > 1:
        x['PurchaseStatus'] = True
        return pd.DataFrame(x.iloc[0]).T
    else:
        return x

unlock_same_month_ = pur_red.groupby(['Symbol', 'ChangeDate']).apply(unlock_same_month)
pur_red = unlock_same_month_.pivot(index='ChangeDate', columns='Symbol', values='PurchaseStatus')

def add_filter(x):
    if (x.isin([1, 2, 3])).any():
        cut_point = x[x == 1].index.append(pd.Index([x.index[0], x.index[-1]])).sort_values()
        cut_interval = np.lib.stride_tricks.sliding_window_view(cut_point, 2)
        result = []
        for one in cut_interval:
            temp = x.loc[one[0] + pd.offsets.MonthEnd(1): one[1]].copy()
            if temp.isin([2, 3]).any():
                temp.loc[temp[temp.isin([2, 3])].index[0]: ] = True
            result.append(temp)
        return pd.concat(result)
    else:
        return x


not_tradable = pur_red.apply(add_filter)
