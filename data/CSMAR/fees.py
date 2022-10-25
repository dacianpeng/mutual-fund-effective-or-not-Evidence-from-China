import dask.dataframe as ddf
import numpy as np
import pandas as pd

csmar_fees = ddf.read_csv('data/CSMAR/fees/*', dtype={'ProportionOfFee': 'object'}).compute()
csmar_fees = csmar_fees[np.logical_or(csmar_fees.NameOfFee == '管理费率', csmar_fees.NameOfFee == '托管费率')]
csmar_fees = csmar_fees.rename(columns={'DeclareDate': 'Date'})
csmar_fees['Date'] = pd.to_datetime(csmar_fees.Date).dt.to_period('M')
csmar_fees['ProportionOfFee'] = csmar_fees.ProportionOfFee.astype(float)
csmar_fees['Symbol'] = csmar_fees.Symbol.astype(str)
csmar_fees = csmar_fees[csmar_fees.ProportionOfFee < 5]