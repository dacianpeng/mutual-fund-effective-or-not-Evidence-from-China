import dask.dataframe as ddf
import pandas as pd

from data.CSMAR.FUND_FundCodeInfo import csmar_symbol_code_mapping

bond_classify = ddf.read_csv('data/CSMAR/bond_classify/*').compute()
bond_classify = pd.merge(bond_classify.drop_duplicates(['MasterFundCode', 'EndDate', 'SpeciesName']), csmar_symbol_code_mapping.drop_duplicates('MasterFundCode'), on='MasterFundCode', how='left')
bond_classify['EndDate']= pd.to_datetime(bond_classify.EndDate).dt.to_period('M')