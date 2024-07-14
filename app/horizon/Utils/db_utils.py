import mysql.connector

from app.db import get_db, close_db
import datetime


# Function to get user ID from auth_key
def get_user_id_from_auth_key(auth_key):
    print(f"getting used id : {auth_key}")

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

    cursor = conn.cursor()

    try:
        cursor.execute("SELECT account_id, account_number, balance, account_type FROM Account WHERE user_id = %s",
                       (user_id,))
        result = cursor.fetchone()

        print(f"\n--- Fetched Details \n--{result}")

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
    print("--- Getting account id for account : " + account_number)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT account_id FROM Account WHERE account_number = %s", (account_number,))
        result = cursor.fetchone()
        if result:
            print(f"--- Account for {account_number} : {result[0]} ")
            return result[0]
        else:
            return None

    except mysql.connector.Error as e:
        print(f"Failed to get account for {account_number}\nDatabase Connection Error")
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
        result = cursor.fetchone()
        print("--- Fetched Account ID ")
        if result:
            print(f"--- Account for {user_id} : {result[0]} ")
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
    print("-- Connecting to the database server")
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT password_hash FROM User WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        if result:
            password_hash = result[0]
            print(f"-- retrived password hash from the database {password_hash}")
            if password_hash == hashed_password:
                return True
            else:
                return False

        else:
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
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM Account WHERE account_id = %s", (account_id,))
        result = cursor.fetchone()
        if result:
            print("--- Fetched account : ")
            print(f"--- Account for {account_id} : {result[0]} ")
            print(result)
            return result

        else:
            return False

    except mysql.connector.Error as e:
        print(f"Error retrieving details {e}")
        return False

    finally:
        cursor.close()
        conn.close()
        close_db()


def store_transaction_in_database(transaction):
    # connects to the database
    print(f"-- Storing transaction in the database")
    conn = get_db()
    cursor = conn.cursor()


def update_account_balance(account_number, new_balance_with_addition):
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

            # Calculate the new balance
            new_balance = new_balance_with_addition

            # Update the balance in the database
            cursor.execute("UPDATE Account SET balance = %s WHERE account_number = %s", (new_balance, account_number))
            conn.commit()

            print(f"--- Updated balance for account number {account_number}: {new_balance}")
            return True
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