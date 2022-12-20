import dask.dataframe as ddf
import pandas as pd

fees = ddf.read_csv('data/CSMAR/fees/*', dtype={'ProportionOfFee': 'object'}).compute()
fees = fees[fees.NameOfFee.isin(['管理费率', '托管费率', '日常赎回费率', '日常申购费率'])]
fees['DeclareDate'] = pd.to_datetime(fees.DeclareDate).dt.to_period('M')
fees = fees[pd.isna(fees['ProportionOfFee'].str.extract(r'([\u4e00-\u9fa5]+)')[0])]
fees['ProportionOfFee'] = fees.ProportionOfFee.str.strip('%').str.strip('？')

fees.groupby(['Symbol', 'DeclareDate']).apply(lambda x: x.ProportionOfFee.astype(float).sum()).to_pickle('data/TwoStepData/fees.pkl')