import dask.dataframe as ddf

csmar_daily_stock = ddf.read_csv('data/CSMAR/daily_stock/*').compute()
