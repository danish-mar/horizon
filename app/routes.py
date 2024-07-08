import jinja2
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from .db import get_db
from .horizon.Security.hash_utils import hash_password
from .horizon.Security.auth_util import generate_auth_key
import mysql.connector

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
    account_name = "Keqing"  # Replace with actual logic to retrieve account details
    account_number = 100210
    account_balance = 20000
    return render_template('account/account.html', account_name=account_name, account_number=account_number,
                           account_balance=account_balance)

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

        # Create the new user in the database
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute('INSERT INTO User (username, password_hash, first_name, last_name, email, phone_number) VALUES (%s, %s, %s, %s, %s, %s)',
                           (username, hashed_password, first_name, last_name, email, phone_number))
            db.commit()
            flash('User created successfully!', 'success')
        except mysql.connector.IntegrityError as err:
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

    return jsonify({'error':'Unauthorized'}),401
    pass


@main.route('/transactions', methods=['GET'])
def get_transactions():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM Products')
    result = cursor.fetchall()
    cursor.close()
    return jsonify({'transactions': result}), 200



@main.route('/transaction/init',methods=['POST'])
def init_transaction():
    return jsonify({'error':'Unauthorized'}),401





# Authentication related endpoints

@main.route('/auth/login', methods=['GET', 'POST'])
def auth():
    if request.method == 'GET':
        return "Requested to view auth page"
    elif request.method == 'POST':
        return "Requested to use auth API"


@main.route('/auth/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'GET':
        return "Requested to view auth page"
    elif request.method == 'POST':
        return "Requested to use auth API"


@main.route('/npi', methods=['GET'])
def render_npi_page():
    return render_template('pages/nyamo/coming_soon.html')


# landing page

@main.route('/', methods=['GET'])
def render_home_page():
    return render_template('index.html')