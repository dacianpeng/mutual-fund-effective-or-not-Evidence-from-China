
import numpy as np
import MySQLdb
from dask import delayed
from sqlalchemy import create_engine

def threaded_df_to_mysql(df, host, user, password, database, port, TABLE_NAME, PARTITIONS, N_WORKERS, THREADS_PER_WORKER):

    df = df.fillna('NULL')
    sql_engine = create_engine(f"mysql://{user}:{password}@{host}:{port}/{database}")
    df.iloc[0: 0].to_sql(TABLE_NAME, sql_engine, if_exists='append', index=False)
    all_parts = np.array_split(df, PARTITIONS)
    def partly_insert(part_sequence):
        '''
        pass
        '''
        part= all_parts[part_sequence]
        con = MySQLdb.connect(host=host, user=user, password=password, database=database, port=port, charset='utf8')
        cursor = con.cursor()
        insert_sql = f"insert into\
    {TABLE_NAME}(`{'`, `'.join(part.columns.values)}`)\
    values\
        {str(list(part.itertuples(index=False, name=None))).strip('[').strip(']')}"

        cursor.execute(insert_sql)
        con.commit()
        con.close()
        return 0

    results = []
    for part_sequence in np.arange(PARTITIONS):
        results.append(delayed(partly_insert)(part_sequence))

    delayed(sum)(results).compute(n_workers=N_WORKERS, threads_per_worker=THREADS_PER_WORKER)