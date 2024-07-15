import unittest
import mysql.connector
import hashlib
from app import db
from app.horizon.Models.Transaction import Transaction

# Function to hash a transaction
def hash_transaction(transaction):
    transaction_data = f"{transaction['transaction_id']}{transaction['account_id']}{transaction['amount']}{transaction['transaction_type']}{transaction['description']}{transaction['created_at']}{transaction['previous_hash']}"
    return hashlib.sha256(transaction_data.encode()).hexdigest()

# Function to check blockchain consistency
def check_blockchain_consistency(cursor):
    try:
        query = "SELECT * FROM Transaction ORDER BY created_at"
        cursor.execute(query)
        transactions = cursor.fetchall()

        if not transactions:
            print("No transactions found.")
            return True

        for i in range(1, len(transactions)):
            previous_transaction = transactions[i - 1]
            current_transaction = transactions[i]

            # Compute the hash of the previous transaction
            expected_previous_hash = hash_transaction(previous_transaction)

            # Compare it with the previous_hash field of the current transaction
            if current_transaction['previous_hash'] != expected_previous_hash:
                print(f"Inconsistency found at transaction ID {current_transaction['transaction_id']}")
                return False

        print("Blockchain is consistent.")
        return True

    except mysql.connector.Error as e:
        print(f"Error checking blockchain consistency: {e}")
        return False

# Unittest class to test the blockchain consistency
class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.mydb = mysql.connector.connect(
            host="cute.denizuh.com",
            user="root",
            password="nahida@dendro123",
            database="nebula"
        )
        self.cursor = self.mydb.cursor(dictionary=True)

    def tearDown(self):
        self.cursor.close()
        self.mydb.close()

    def test_something(self):
        self.cursor.execute("SELECT * FROM Transaction LIMIT 1")
        result = self.cursor.fetchone()
        print(result)
        transaction = Transaction.from_db_result(result)
        print(transaction)

    def test_blockchain_consistency(self):
        self.assertTrue(check_blockchain_consistency(self.cursor), "Blockchain is not consistent")

if __name__ == '__main__':
    unittest.main()
