
import MySQLdb

def set_mysql_table_index(host, user, password, database, port, TABLE_NAME, INDEXES):
    db = MySQLdb.connect(host=host, user=user, password=password, database=database, port=port)
    cursor = db.cursor()
    cursor.execute(f'ALTER TABLE `{TABLE_NAME}` ADD INDEX ({INDEXES})')