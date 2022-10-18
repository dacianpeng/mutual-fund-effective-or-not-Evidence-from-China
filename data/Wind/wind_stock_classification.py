
import pandas as pd


wind_stock_classification = pd.read_excel('data/Wind/wind_classification.xlsx')
wind_stock_classification['证券代码'] = wind_stock_classification.证券代码.str.split('.').str[0]
wind_stock_classification['证券代码'] = wind_stock_classification.证券代码.astype(int)
csrc_stock_classification = wind_stock_classification.iloc[:, [0, 3]]
csrc_stock_classification.columns = ['Stkcd', 'Indnme']

wind_stock_classification = wind_stock_classification.iloc[:, [0, 4]]
wind_stock_classification.columns = ['Stkcd', 'Indnme']