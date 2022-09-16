import psycopg2
from config import host, user, password, db_name
import sqlcommands


try:
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    with connection.cursor() as cursor:
        cursor.execute(sqlcommands.select_max_difference)
        for row in cursor:
            print(row)
        # connection.commit()
except Exception as ex:
    if ex.args[0] == 1062:
        print("Goods are already in the database")
    else:
        print('Connection error...')
        print(ex)
finally:
    connection.close()
