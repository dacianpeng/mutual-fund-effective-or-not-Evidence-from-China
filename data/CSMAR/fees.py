import dask.dataframe as ddf
import numpy as np
import pandas as pd

csmar_fees = ddf.read_csv('data/CSMAR/fees/*', dtype={'ProportionOfFee': 'object'}).compute()
csmar_fees = csmar_fees[csmar_fees.NameOfFee.isin(['日常申购费率', '日常赎回费率', '管理费率', '托管费率'])]
csmar_fees = csmar_fees.rename(columns={'DeclareDate': 'Date'})
csmar_fees['Date'] = pd.to_datetime(csmar_fees.Date).dt.to_period('M')

import re
def check_汉字(str):
    return bool(re.findall(r'([\u4e00-\u9fa5]+)', str))

csmar_fees.loc[csmar_fees.ProportionOfFee.apply(lambda x: check_汉字(str(x))), 'ProportionOfFee'] = 1.0
csmar_fees['ProportionOfFee'] = csmar_fees.ProportionOfFee.str.strip('%')
csmar_fees['ProportionOfFee'] = csmar_fees.ProportionOfFee.str.strip('？')

csmar_fees['ProportionOfFee'] = csmar_fees.ProportionOfFee.astype(float)
csmar_fees['Symbol'] = csmar_fees.Symbol.astype(str)
csmar_fees = csmar_fees[csmar_fees.ProportionOfFee < 5]