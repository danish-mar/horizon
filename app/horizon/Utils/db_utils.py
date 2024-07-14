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
    print(f"Getting account details from the server for user id {user_id}")
    conn = get_db()

    cursor = conn.cursor()

    try:
        cursor.execute("SELECT account_id, account_number, balance, account_type FROM Account WHERE user_id = %s",
                       (user_id,))
        result = cursor.fetchone()

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
from mysql.connector import Error


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
