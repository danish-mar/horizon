from datetime import datetime, timedelta
import random
from decimal import Decimal

import jinja2
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session, make_response
from .db import get_db
from .horizon.Models.Transaction import Transaction
from .horizon.Security.hash_utils import hash_password, confirm_password_hash
from .horizon.Security.auth_util import generate_auth_key
import mysql.connector

from .horizon.Utils.db_utils import *

main = Blueprint('main', __name__)


@main.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # Process the contact form data here
        flash('Your message has been sent!', 'success')
        return redirect(url_for('main.index'))
    return render_template('contact.html')


# All routes releted to account
@main.route('/account', methods=['GET'])
def account_view():
    auth_key = request.cookies.get('X-Auth-Token')
    print(f"---- Retrived Auth-Key : {auth_key}")
    print(f"---- Checking Token Expiration...")
    # if not auth_key or not check_authkey_expiration(auth_key) or not get_user_id_from_auth_key(auth_key):
    #     return redirect(url_for('main.auth'))
    if not auth_key:
        return redirect(url_for('main.auth'))
    if not check_authkey_expiration(auth_key):
        return redirect(url_for('main.auth'))

    user_id = get_user_id_from_auth_key(auth_key)

    # if auth_key:
    #     if check_authkey_expiration(auth_key):
    #         return redirect(url_for('main.auth'))

    # user_id = get_user_id_from_auth_key(auth_key)
    # # print(user_id)
    # if not user_id:
    #      return redirect('/auth/login')
    close_db()
    account_details = get_account_details_from_database(user_id)
    close_db()
    user_details = get_user_details_from_database_by_id(user_id)
    print(user_details)

    if not account_details:
        return render_template('account/account_not_found.html')

    # Unpack the details correctly
    account_name = user_details[1]  # Assuming this is the username or user's full name
    print(user_details[1] + " : " + account_name)
    account_number = account_details['account_number']  # Access by key
    account_balance = account_details['account_balance']  # Access by key
    account_type = account_details['account_type']

    return render_template('account/account.html', last_name=account_name.capitalize(), account_number=account_number,
                           account_balance=account_balance, account_type=account_type)


@main.route('/account/create', methods=['GET', 'POST'])
def create_account():
    if request.method == 'GET':
        return render_template('account/create_account.html')

    elif request.method == 'POST':
        username = request.form.get('username')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Basic validation
        if not username or not first_name or not last_name or not email or not password or not confirm_password:
            flash('All fields except phone number are required!', 'error')
            return redirect(url_for('main.create_account'))

        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('main.create_account'))

        # Hash the password
        hashed_password = hash_password(password)

        # Generate a random account number (example implementation)
        account_number = ''.join(str(random.randint(0, 9)) for _ in range(10))

        # Default account type to 'savings'
        account_type = request.form.get('account_type', 'savings')

        # Initial balance
        initial_balance = 0.00

        # Current timestamp
        created_at = datetime.now()

        # Create the new user in the database
        db = get_db()
        cursor = db.cursor()
        try:
            # Insert user data
            cursor.execute(
                'INSERT INTO User (username, password_hash, first_name, last_name, email, phone_number) VALUES (%s, %s, %s, %s, %s, %s)',
                (username, hashed_password, first_name, last_name, email, phone_number))
            user_id = cursor.lastrowid  # Get the last inserted user_id

            # Insert account data linked to the user
            cursor.execute(
                'INSERT INTO Account (user_id, account_number, account_type, balance, created_at) VALUES (%s, %s, %s, %s, %s)',
                (user_id, account_number, account_type, initial_balance, created_at))

            db.commit()
            flash('User created successfully!', 'success')
            return redirect('/auth/login')
        except mysql.connector.Error as err:
            db.rollback()
            flash(f'Error: {err}', 'error')
        finally:
            cursor.close()

        return redirect(url_for('main.create_account'))


@main.route('/account/update', methods=['GET', 'POST'])
def update_account_info():
    if request.method == 'GET':
        return "Requested to view account creationg page"  # returns the account update page
    elif request.method == 'POST':
        return "Requested to use account creation API"  # returns the result of the API


@main.route('/account/<int:account_id>', methods=['GET'])
def get_account_details(account_id):
    # Implement authentication logic here
    # Check if the provided auth key is valid and linked to the requested account_id
    if not is_authorized(account_id, request.headers.get('Authorization')):
        return jsonify({'error': 'Unauthorized'}), 401

    # Assuming successful authentication, retrieve account details
    account_details = get_account_info(account_id)  # Replace with actual retrieval logic

    # Check if account exists
    if not account_details:
        return jsonify({'error': 'Account not found'}), 404

    # Return account details
    return jsonify(account_details), 200


# Helper functions (replace with your actual implementation)
def is_authorized(account_id, auth_key):
    # Implement logic to validate the auth key and its association with account_id
    # This might involve checking a database or using a token-based authentication system
    pass


def get_account_info(account_id):
    # Implement logic to retrieve account details from a database or other data source
    # based on the provided account_id
    pass


@main.route('/account/link', methods=['POST'])
def link_account():
    # logic to link an account to a customer
    pass


# Transaction related Endpoints

@main.route('/transactions/<int:transaction_id>', methods=['GET'])
def get_related_transaction(transaction_id):
    # implement a logic to validate the relativeness and return the data into json format

    return jsonify({'error': 'Unauthorized'}), 401
    pass


@main.route('/transactions', methods=['GET'])
def get_transactions():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM Transaction')
    result = cursor.fetchall()
    cursor.close()
    return jsonify({'transactions': result}), 200


@main.route('/transaction/new', methods=['POST', 'GET'])
def init_transaction():
    auth_key = request.cookies.get('X-Auth-Token')

    # first lets get the details of the transaction:
    if request.method == 'GET':
        # if not auth_key:
        #     return redirect(url_for('main.auth'))
        # if check_authkey_expiration(auth_key):
        #     return render_template("account/new_transaction.html")
        # else:
        #     return render_template("account/login.html")

        if auth_key and check_authkey_expiration(auth_key):
            return render_template("/account/new_transaction.html")
        else:
            return redirect("/auth/login")

    if request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Missing data'}), 400

        # necessary details to make the transaction
        user_id = get_user_id_from_auth_key(auth_key)
        initiater_account_id = get_account_id_from_user_id(user_id)

        # fetches the account details from the client

        reciever_account_number = data.get('reciever_account')
        amount_to_be_sent = Decimal(data.get('amount'))
        description = data.get('description')
        unencrypted_password = data.get('unencrypted_password')

        transaction_data = {
            'reciever_account': data.get('reciever_account'),
            'amount': data.get('amount'),
            'description': data.get('description'),
        }

        print(f"---( Got New Transaction Request ) : {transaction_data}")

        # encrypts and compare the password

        client_hashed_password = hash_password(unencrypted_password)

        # gets the password from the database and validate it
        if check_user_password(user_id,unencrypted_password):
            # upon successful validation make a transaction
            print("-- Authentication Successfull")
            # gets the initiater's account details
            initiater_account_details = get_account_details_from_database(user_id)
            print(initiater_account_details)
            # get's the account balance from the initiater's account
            initiater_account_balance = initiater_account_details['account_balance']
            print(initiater_account_balance)
            # compare the balance with the amount to be transfered
            print(type(initiater_account_balance))
            print(type(amount_to_be_sent))
            if initiater_account_balance < amount_to_be_sent:
                # returns insufficient balance due to lack of balance in the account
                return jsonify({'error': 'Insufficient balance'}), 401
            elif initiater_account_balance > amount_to_be_sent:
                # process the transaction
                reciever_account_id = get_account_id_from_account_number(reciever_account_number)
                # gets the account id and turn it into an object
                reciever_account_object = get_account_from_id(reciever_account_id)
                # extract account balance
                reciever_current_account_balance = reciever_account_object[4]
                # adds the amount to it
                # reciever_account_new_balance = reciever_current_account_balance + amount_to_be_sent
                # initiater_account_new_balance = initiater_account_balance - amount_to_be_sent
                # updates the amounts on the database server
                credit(reciever_account_number, amount_to_be_sent)
                debit(initiater_account_details['account_number'], amount_to_be_sent)

                current_date_time = datetime.datetime.now()
                print("--- Transaction partially completed ")
                # creates a new transaction to update on the transaction database
                print("--- Updating blockchain on the database server")
                # create's the debit transaction
                last_transaction_hash = get_last_transaction().calculate_hash()
                # on the basis of this create the transaction details
                insert_transaction(initiater_account_id,reciever_account_id,amount_to_be_sent,"debit",description,last_transaction_hash)
                new_last_transaction_hash = get_last_transaction().calculate_hash()
                # now for the credited account
                insert_transaction(initiater_account_id,reciever_account_id,amount_to_be_sent,"credit",description,new_last_transaction_hash)
                #completed
                print("--- Transaction fully completed")
                return jsonify({'error': 'Transaction Completed'}), 200
    else:
        return jsonify({'error': 'Unauthorized'}), 401


# Authentication related endpoints

@main.route('/auth/login', methods=['GET', 'POST'])
def auth():
    if request.method == 'GET':
        return render_template('account/login.html')
    elif request.method == 'POST':
        data = request.get_json()  # Parse JSON data from request body
        if not data:
            return jsonify({'success': False, 'message': 'Invalid data'}), 400

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'success': False, 'message': 'Username and password are required'}), 400

        try:
            db = get_db()
            cursor = db.cursor(dictionary=True)
            cursor.execute('SELECT * FROM User WHERE username = %s', (username,))
            user = cursor.fetchone()

            if user:
                print(f"Retrieved user: {user}")
                password_hash = user.get('password_hash')
                print(f"Password hash from database: {password_hash}")

                if password_hash and confirm_password_hash(password_hash, password):
                    auth_key = generate_auth_key()
                    expiry_timestamp = datetime.datetime.now() + timedelta(minutes=30)
                    cursor.execute(
                        'INSERT INTO Auth_Key (auth_key, user_id, expiry_timestamp) VALUES (%s, %s, %s)',
                        (auth_key, user['user_id'], expiry_timestamp)
                    )
                    db.commit()

                    response_data = {
                        'success': True,
                        'message': 'Login successful'
                    }
                    response = jsonify(response_data)
                    response.headers['X-Auth-Token'] = auth_key
                    print(response)
                    return response, 200
                else:
                    response_data = {
                        'success': False,
                        'message': 'Invalid username or password'
                    }
                    print(response_data)
                return jsonify(response_data), 401
            else:
                response_data = {
                    'success': False,
                    'message': 'Invalid username or password'
                }
                return jsonify(response_data), 401
        except mysql.connector.errors.DatabaseError:
            print("[!] Database Servers are down!")
            response_data = {
                'success': False,
                'server_response_code': 503,
                "message": "We're sorry for the inconvenience 😢\nOur servers are currently being maintained 🛠️\nPlease try again later! 💖"
            }
            print(response_data)
            return jsonify(response_data), 405


@main.route('/auth/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'GET':
        # Render a dark-themed confirmation page
        return render_template('account/logout_confirmation.html')
    elif request.method == 'POST':
        # Clear the Auth-Token cookie
        response = make_response("""
        <html>
        <body style="background-color: #333; color: #fff; text-align: center; font-family: Arial, sans-serif;">
            <h1>Logged out successfully</h1>
            <p>Redirecting to home page...</p>
            <script>
                setTimeout(function() {
                    window.location.href = "/";
                }, 2000);
            </script>
        </body>
        </html>
        """)
        response.set_cookie('X-Auth-Token', '', expires=0)
        return response


@main.route('/npi', methods=['GET'])
def render_npi_page():
    return render_template('pages/nyamo/coming_soon.html')


# landing page

@main.route('/', methods=['GET'])
def render_home_page():
    return render_template('index.html')


@main.route('/check_authentication')
def check_authentication():
    auth_key = request.cookies.get('X-Auth-Token')  # Get X-auth-key from cookies or headers
    if auth_key:
        # Perform your authentication logic here
        # For example, check if auth_key is valid in your database or session
        authenticated = True  # Replace with your actual authentication check
    else:
        authenticated = False

    return jsonify({'authenticated': authenticated})
