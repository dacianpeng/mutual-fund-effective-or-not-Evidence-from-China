
import dask.dataframe as ddf
import numpy as np
import pymysql
from dask import delayed
from sqlalchemy import create_engine
import pandas as pd



df_to_be_insert = ddf.read_csv('data/CSMAR/invest_detail/*', low_memory=False, dtype={'Symbol': 'object'}).compute()
df_to_be_insert = df_to_be_insert.fillna('NULL')

TABLE_NAME = 'FUND_NAV'
# TABLE_NAME = 'FUND_MainInfo'
# df_to_be_insert = pd.read_csv(f'data/CSMAR/{TABLE_NAME}.csv')

sql_engine = create_engine("mysql://root:Doushi0930!@dacian.cc:38322/csmar")
df_to_be_insert.iloc[0: 0].to_sql(TABLE_NAME, sql_engine, if_exists='append')
PARTITIONS = 1000
N_WORKERS = 8

def split_equal(value, parts):
    '''
    split a number into parts interval
    '''
    value = float(value)
    return [round(i * value / parts) for i in range(0, parts + 1)]

all_parts = split_equal(len(df_to_be_insert), PARTITIONS)

def partly_insert(this_part_sequence):
    '''
    a really cool toy
    '''
    part= df_to_be_insert.iloc[all_parts[this_part_sequence]: all_parts[this_part_sequence + 1]]
    con = pymysql.connect(host='dacian.cc', user='root', password="Doushi0930!",
                           database='csmar', port=38321,
                           charset='utf8')
    cursor = con.cursor()
    insert_sql = f"insert into\
 {TABLE_NAME}(`{'`, `'.join(part.columns.values)}`)\
 values\
    {str(list(part.itertuples(index=False, name=None))).strip('[').strip(']')}"


    cursor.execute(insert_sql)
    con.commit()

    return 0


results = []
for this_part_sequence in np.arange(PARTITIONS):
    results.append(delayed(partly_insert)(this_part_sequence))

delayed(sum)(results).compute(n_workers=N_WORKERS)
