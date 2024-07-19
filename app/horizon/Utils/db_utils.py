import mysql.connector
from app.horizon.Models.Transaction import *
from app.db import get_db, close_db
import datetime

from app.horizon.Security.hash_utils import *


# Function to get user ID from auth_key
def get_user_id_from_auth_key(auth_key):
    print(f"getting user id for : {auth_key}")

    db = get_db()

    db.reconnect()

    cursor = db.cursor()

    try:
        cursor.execute("SELECT user_id FROM Auth_Key WHERE auth_key = %s", (auth_key,))
        result = cursor.fetchone()
        print("Getting user id from auth key")
        print(result[0])
        close_db()
        if result:
            return result[0]
        return None
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("[i] Access Denied to the database")
            return None
    finally:
        cursor.close()
        db.close()


# Function to get account details from user ID
def get_account_details_from_database(user_id):
    print(f"---- Getting account details from the server for user id {user_id}")
    conn = get_db()
    conn.reconnect()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT account_id, account_number, balance, account_type FROM Account WHERE user_id = %s",
                       (user_id,))
        result = cursor.fetchone()

        print(f"--- Querying : {cursor.rowcount} rows")

        print(f"\n--- Fetched Details \n--")
        print(result)

        if result:
            return {
                'account_name': result[0],
                'account_number': result[1],
                'account_balance': result[2],
                'account_type': result[3]
            }
        return None
    except mysql.connector.Error as err:
        print(err, err.errno)

    finally:
        cursor.close()
        conn.close()


# Function to get user deatils but user id
import mysql.connector


def get_user_details_from_database_by_id(user_id):
    conn = get_db()
    print("Getting user details from database")
    if conn is None:
        print("connection is null")
        return None  # Handle connection error here

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT username, first_name, last_name, email, phone_number FROM User WHERE user_id = %s",
                       (user_id,))
        result = cursor.fetchone()
        return result
    except mysql.connector.Error as e:
        print(f"Error retrieving user details: {e}")
        return None
    finally:
        cursor.close()
        conn.close()
        close_db()


def check_authkey_expiration(auth_key):
    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM Auth_Key WHERE auth_key = %s", (auth_key,))
        result = cursor.fetchone()

        if result:
            expiration_date = result[2]
            print(f"{expiration_date} : {datetime.datetime.now()}")

            if expiration_date > datetime.datetime.now():
                return True
            else:
                return False
        else:
            return False
    except mysql.connector.Error as e:
        print(f"Error retrieving Auth Key Details: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
        close_db()


def get_account_id_from_account_number(account_number):
    conn = get_db()
    print(f"--- Getting account id for account : {account_number} ")
    conn.reconnect()
    cursor = conn.cursor()
    try:
        int_account_number = int(account_number)
        cursor.execute("SELECT account_id FROM Account WHERE account_number = %s", (account_number,))
        result = cursor.fetchone()
        if result:
            print(f"--- Account for {account_number} : {result[0]} ")
            return result[0]
        else:
            return None

    except mysql.connector.Error as e:
        print(f"Failed to get account for {account_number}\nError retrieving details of account: {e}")
        return None

    finally:
        cursor.close()
        conn.close()
        close_db()


def get_account_id_from_user_id(user_id):
    conn = get_db()
    print(f"--- Getting account for user {user_id}")
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT account_id FROM Account WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        print("--- Fetched Account ID ")
        if result:
            print(f"--- Account ID for {user_id} : {result[0]}")
            return result[0]
        return None

    except mysql.connector.Error as err:
        print(err)

    finally:
        cursor.close()
        conn.close()


def check_user_password(user_id, hashed_password):
    print(f"--- checking password for account {user_id} with hashed password {hashed_password}")
    conn = get_db()
    conn.reconnect()
    print("-- Connecting to the database server")
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT password_hash FROM User WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        if result:
            password_hash = result[0]
            print(f"-- retrived password hash from the database {password_hash} : {hashed_password}")
            if confirm_password_hash(password_hash, hashed_password):
                print("--- Matched")
                return True
            else:
                print("--- Not Matched")
                return False

        else:
            print("--- failed")
            return False

    except mysql.connector.Error as e:
        print(f"Error retrieving details {e}")
        return False

    finally:
        cursor.close()
        conn.close()
        close_db()


def get_account_from_id(account_id):
    print(f"--- getting account from account id {account_id}")
    conn = get_db()
    print("-- Connecting to the database server")
    conn.reconnect()
    if conn.is_connected():
        print("--- database is still connected")
    else:
        print("--- database disconnected")

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Account WHERE user_id = %s", (account_id,))
        print(cursor.fetchall())
        result = cursor.fetchone()
        print(result)
        if result:
            print("--- Fetched account : ")
            print(f"--- Account for {account_id} : {result[0]} ")
            print(result)
            return result
        else:
            print("--- Error Fetching Data")
            return None

    except mysql.connector.Error as e:
        print(f"Error retrieving details {e}")
        return False

    finally:
        cursor.close()
        conn.close()
        close_db()


def credit(to_account_number, from_account_number, add_balance, description):
    print(f"--- updating account balance for account number {to_account_number}")
    conn = get_db()
    print("-- Connecting to the database server")
    cursor = conn.cursor()

    try:
        # Get the current balance
        cursor.execute("SELECT balance FROM Account WHERE account_number = %s", (to_account_number,))
        result = cursor.fetchone()

        if result:
            # On first let it credit
            current_balance = result[0]
            print(f"--- Current balance for account number {to_account_number}: {current_balance}")

            # Calculate the new balance
            new_balance = current_balance + add_balance

            # Update the balance in the database
            cursor.execute("UPDATE Account SET balance = %s WHERE account_number = %s",
                           (new_balance, to_account_number))
            conn.commit()

            print(f"--- Updated balance for account number {to_account_number}: {new_balance}")

            print(f"--- Updating Transaction table")
            insert_transaction(to_account_number, add_balance, "credit", description,
                               get_last_transaction().calculate_hash())
            return True
        else:
            print(f"--- No account found with account number {to_account_number}")
            return False

    except mysql.connector.Error as e:
        print(f"Error updating account balance: {e}")
        return False

    finally:
        cursor.close()
        conn.close()
        close_db()


def credit_account(to_account_number, from_account_number, add_balance, description, platform):
    print(f"--- Updating account balance for account number {to_account_number}")
    conn = get_db()
    print("-- Connecting to the database server")
    cursor = conn.cursor()

    try:
        # Get the current balance of to_account
        cursor.execute("SELECT balance FROM Account WHERE account_number = %s", (to_account_number,))
        to_result = cursor.fetchone()

        # Get the current balance of from_account
        cursor.execute("SELECT balance FROM Account WHERE account_number = %s", (from_account_number,))
        from_result = cursor.fetchone()

        if to_result and from_result:
            # On first let it credit
            to_current_balance = to_result[0]
            from_current_balance = from_result[0]
            print(f"--- Current balance for account number {to_account_number}: {to_current_balance}")
            print(f"--- Current balance for account number {from_account_number}: {from_current_balance}")

            # Calculate the new balances
            to_new_balance = to_current_balance + add_balance
            from_new_balance = from_current_balance - add_balance

            if from_new_balance < 0:
                print(f"--- Insufficient funds in account number {from_account_number}")
                return False

            # Update the balances in the database
            cursor.execute("UPDATE Account SET balance = %s WHERE account_number = %s",
                           (to_new_balance, to_account_number))
            cursor.execute("UPDATE Account SET balance = %s WHERE account_number = %s",
                           (from_new_balance, from_account_number))
            conn.commit()

            print(f"--- Updated balance for account number {to_account_number}: {to_new_balance}")
            print(f"--- Updated balance for account number {from_account_number}: {from_new_balance}")
            print(f"--- Updating Transaction table")
            insert_transaction_account(to_account_number, from_account_number, to_account_number, add_balance, "credit", description, get_last_transaction().calculate_hash(), platform)
            return True
        else:
            if not to_result:
                print(f"--- No account found with account number {to_account_number}")
            if not from_result:
                print(f"--- No account found with account number {from_account_number}")
            return False

    except mysql.connector.Error as e:
        print(f"Error updating account balance: {e}")
        return False

    finally:
        cursor.close()
        conn.close()
        close_db()


def debit(account_number, subtract_balance, description):
    print(f"--- updating account balance for account number {account_number}")
    conn = get_db()
    print("-- Connecting to the database server")
    cursor = conn.cursor()

    try:
        # Get the current balance
        cursor.execute("SELECT balance FROM Account WHERE account_number = %s", (account_number,))
        result = cursor.fetchone()

        if result:
            current_balance = result[0]
            print(f"--- Current balance for account number {account_number}: {current_balance}")

            # Check if the balance is sufficient for the debit
            if current_balance >= subtract_balance:
                # Calculate the new balance
                new_balance = current_balance - subtract_balance

                # Update the balance in the database
                cursor.execute("UPDATE Account SET balance = %s WHERE account_number = %s",
                               (new_balance, account_number))
                conn.commit()

                print(f"--- Updated balance for account number {account_number}: {new_balance}")

                print(f"--- Updating records")

                insert_transaction(account_number, subtract_balance, "debit", description,
                                   get_last_transaction().calculate_hash())

                return True
            else:
                print(f"--- Insufficient balance for account number {account_number}")
                return False
        else:
            print(f"--- No account found with account number {account_number}")
            return False

    except mysql.connector.Error as e:
        print(f"Error updating account balance: {e}")
        return False

    finally:
        cursor.close()
        conn.close()
        close_db()


def debit_account(from_account_number, to_account_number, subtract_balance, description, platform):
    print(
        f"--- {platform} :  Updating account balances for account number {from_account_number} (debit) and {to_account_number} (credit)")
    conn = get_db()
    print("-- Connecting to the database server")
    cursor = conn.cursor()

    try:
        # Get the current balance of from_account
        cursor.execute("SELECT balance FROM Account WHERE account_number = %s", (from_account_number,))
        from_result = cursor.fetchone()

        # Get the current balance of to_account
        cursor.execute("SELECT balance FROM Account WHERE account_number = %s", (to_account_number,))
        to_result = cursor.fetchone()

        if from_result and to_result:
            from_current_balance = from_result[0]
            to_current_balance = to_result[0]
            print(f"--- Current balance for account number {from_account_number}: {from_current_balance}")
            print(f"--- Current balance for account number {to_account_number}: {to_current_balance}")

            # Check if the balance is sufficient for the debit
            if from_current_balance >= subtract_balance:
                # Calculate the new balances
                from_new_balance = from_current_balance - subtract_balance
                to_new_balance = to_current_balance + subtract_balance

                # Update the balances in the database
                cursor.execute("UPDATE Account SET balance = %s WHERE account_number = %s",
                               (from_new_balance, from_account_number))

                cursor.execute("UPDATE Account SET balance = %s WHERE account_number = %s",
                               (to_new_balance, to_account_number))
                conn.commit()

                print(f"--- Updated balance for account number {from_account_number}: {from_new_balance}")
                print(f"--- Updated balance for account number {to_account_number}: {to_new_balance}")

                print(f"--- Updating Transaction table")
                # insert_transaction(from_account_number, to_account_number, subtract_balance, "debit", description,
                #                    get_last_transaction().calculate_hash())
                insert_transaction_account(from_account_number,from_account_number, to_account_number, subtract_balance, "debit", description, get_last_transaction().calculate_hash(), platform)

                return True
            else:
                print(f"--- Insufficient balance for account number {from_account_number}")
                return False
        else:
            if not from_result:
                print(f"--- No account found with account number {from_account_number}")
            if not to_result:
                print(f"--- No account found with account number {to_account_number}")
            return False

    except mysql.connector.Error as e:
        print(f"Error updating account balance: {e}")
        return False

    finally:
        cursor.close()
        conn.close()
        close_db()


def get_last_transaction():
    print(f"--- Getting last transaction from the database")
    conn = get_db()
    print("-- Connecting to the database server")
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM Transaction ORDER BY created_at DESC LIMIT 1")
        result = cursor.fetchone()

        if result:
            print("--- Last transaction details:")
            print(result)
            last_transaction = Transaction.from_db_result(result)
            return last_transaction
        else:
            print("--- No transactions found")
            return None

    except mysql.connector.Error as e:
        print(f"Error retrieving last transaction: {e}")
        return None

    finally:
        cursor.close()
        conn.close()
        close_db()


def get_account_id_by_account_number(account_number, conn, cursor):
    try:
        query = "SELECT account_id FROM Account WHERE account_number = %s"
        print(f"--- Executing: {query} with parameter: {account_number}")
        cursor.execute(query, (account_number,))
        result = cursor.fetchone()
        if result:
            print("--- fetched account ID")
            return result[0]
        else:
            return None
    except mysql.connector.Error as e:
        print(f"Error retrieving account ID: {e}")
        return None


def insert_transaction(account_number, amount, transaction_type, description, previous_hash):
    print(f"--- Inserting transaction into the database")
    conn = get_db()
    conn.reconnect()
    cursor = conn.cursor()

    try:
        # Fetch account_id using the provided account_number
        account_id = get_account_id_by_account_number(account_number, conn, cursor)
        if not account_id:
            print("Error: Account ID not found.")
            return None

        query = """
        INSERT INTO Transaction (account_id, amount, transaction_type, description, previous_hash)
        VALUES (%s, %s, %s, %s, %s);
        """
        cursor.execute(query, (account_id, amount, transaction_type, description, previous_hash))
        conn.commit()  # Commit the transaction

        print("--- Transaction inserted successfully")
        return cursor.lastrowid  # Return the ID of the inserted row

    except mysql.connector.Error as e:
        print(f"Error inserting transaction: {e}")
        return None
    finally:
        cursor.close()
        conn.close()
        close_db()


def insert_transaction_account(initiator_account_number, from_account_number, to_account_number, amount,
                               transaction_type, description, previous_hash, platform):
    global from_account_id, to_account_id

    print(f"--- Inserting transaction into the database")
    conn = get_db()
    conn.reconnect()
    cursor = conn.cursor()

    try:
        # Fetch account IDs using the provided account numbers
        initiator_account_id = get_account_id_by_account_number(initiator_account_number, conn, cursor)


        query = """
        INSERT INTO Transaction (account_id, amount, transaction_type, description, previous_hash, to_account, from_account, platform)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(query, (
        initiator_account_id, amount, transaction_type, description, previous_hash, to_account_number, from_account_number, platform))
        conn.commit()  # Commit the transaction

        print("--- Transaction inserted successfully")
        return cursor.lastrowid  # Return the ID of the inserted row

    except mysql.connector.Error as e:
        print(f"Error inserting transaction: {e}")
        return None
    finally:
        cursor.close()
        conn.close()
        close_db()


def get_account_user_id_by_account_id(account_id):
    conn = get_db()
    cursor = conn.cursor()
    conn.reconnect()
    try:
        query = "SELECT user_id FROM Account WHERE account_id = %s"
        print(f"Executing: {query} with parameter: {account_id}")
        cursor.execute(query, (account_id,))
        result = cursor.fetchone()
        if result:
            print("--- fetched account owner id")
            return result[0]
        else:
            return None
    except mysql.connector.Error as e:
        print(f"Error retrieving details of account: {e}")
        return None

    finally:
        cursor.close()
        conn.close()
        close_db()


def get_userdetails_from_account_number(account_number):
    account_id = get_account_id_from_account_number(account_number)
    owner_id = get_account_user_id_by_account_id(account_id)
    user_details = get_user_details_from_database_by_id(owner_id)
    return user_details


def is_auth_key(auth_key):
    conn = get_db()
    cursor = conn.cursor()
    conn.reconnect()
    try:
        query = "SELECT * FROM Auth_Key WHERE auth_key = %s"
        print(f" Executing : {query} with parameter: {auth_key}")
        cursor.execute(query, (auth_key,))
        result = cursor.fetchone()
        if result:
            auth_expiration_date = result[2]
            if auth_expiration_date > datetime.datetime.now():
                print("--- Authorized")
                return True
            else:
                return False
        else:
            return False

    except mysql.connector.Error as e:
        print(f"Error verifying auth key {auth_key}")
        print(e)
        return False

    finally:
        if conn.is_connected():
            print("--- Closing Connection")
            cursor.close()
            conn.close()
            close_db()
