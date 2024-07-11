import unittest
import mysql.connector
from app import db
from app.horizon.Models.Transaction import Transaction



# some python code to check if the class is working or not
class MyTestCase(unittest.TestCase):
    def test_something(self):
        mydb = mysql.connector.connect(
            host="cute.denizuh.com",
            user="root",
            password="nahida@dendro123",
            database="nebula"
        )

        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM Transaction")
        result = cursor.fetchone()
        transaction = Transaction.from_db_result(result)

        print(transaction.__str__())



if __name__ == '__main__':
    unittest.main()
