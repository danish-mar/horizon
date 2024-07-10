import mysql.connector

from app.db import get_db, close_db


# Function to get user ID from auth_key
def get_user_id_from_auth_key(auth_key):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT user_id FROM Auth_Key WHERE auth_key = %s", (auth_key,))
    result = cursor.fetchone()
    cursor.close()
    close_db()
    if result:
        return result[0]
    return None


# Function to get account details from user ID
def get_account_details_from_database(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT account_id, account_number, balance, account_type FROM Account WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    conn.close()
    close_db()

    print(result)

    if result:
        return {
            'account_name': result[0],
            'account_number': result[1],
            'account_balance': result[2],
            'account_type': result[3]
        }
    return None


# Function to get user deatils but user id
import mysql.connector
from mysql.connector import Error

def get_user_details_from_database_by_id(user_id):
    conn = get_db()
    if conn is None:
        return None  # Handle connection error here

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT username, first_name, last_name, email, phone_number FROM User WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        return result
    except mysql.connector.Error as e:
        print(f"Error retrieving user details: {e}")
        return None
    finally:
        cursor.close()
        conn.close()
        close_db()

