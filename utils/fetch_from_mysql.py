import MySQLdb
import pandas as pd

def fetch_from_mysql(host, user, password, database, port, TABLE_NAME, SQL):

    db = MySQLdb.connect(host=host, user=user, password=password, database=database, port=port)
    cursor = db.cursor()
    cursor.execute(f'select column_name from information_schema.columns where table_name="{TABLE_NAME}"')
    columns = list(map(lambda x: x[0], cursor.fetchall()))
    cursor.execute(SQL)
    data = pd.DataFrame(cursor.fetchall(), columns=columns)

    return data