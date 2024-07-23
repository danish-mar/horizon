import unittest

import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(
        host='cute.denizuh.com',
        database='nebula',
        user='root',
        password='nahida@dendro123'
    )
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()

        # Fetch the current database name
        cursor.execute("SELECT DATABASE()")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

        # Fetch specific transaction details
        cursor.execute("SELECT * FROM Transaction WHERE account_id = 1 AND transaction_id = 29")
        record1 = cursor.fetchone()
        print("Transaction details (ID 29):", record1)
except Error as e:
    print("Error while connecting to MySQL", e)

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
