
import dask.dataframe as ddf
import numpy as np
import pymysql
from dask import delayed
from sqlalchemy import create_engine

df = ddf.read_csv('data/CSMAR/invest_detail/*', low_memory=False, dtype={'Symbol': 'object'}).compute()
df = df.fillna('NULL')

TABLE_NAME = 'IDX_Smprat'


sql_engine = create_engine("mysql://root:Doushi0930!@dacian.cc:38322/csmar")
df.iloc[0: 0].to_sql(TABLE_NAME, sql_engine, if_exists='append')
PARTITIONS = 1000
N_WORKERS = 8

all_parts = np.array_split(df, PARTITIONS)

def partly_insert(part_sequence):
    '''
    pass
    '''
    part= df.iloc[all_parts[part_sequence]: all_parts[part_sequence + 1]]
    con = pymysql.connect(host='localhost', user='root', password="Doushi0930!",
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
