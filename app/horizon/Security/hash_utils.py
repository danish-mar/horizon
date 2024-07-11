import bcrypt


def hash_password(password):
    """
    Hashes a password securely using bcrypt.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The hashed password string.
    """
    # Encode the password to bytes as bcrypt expects bytes
    password_bytes = password.encode('utf-8')
    # Generate a random salt using bcrypt
    salt = bcrypt.gensalt()
    # Hash the password with the generated salt
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    # Return the hashed password as a UTF-8 encoded string
    return hashed_password.decode('utf-8')


def confirm_password_hash(hashed_password, password):
    """
    Checks if the provided password matches the hashed password.

    Args:
        hashed_password (str): The hashed password string.
        password (str): The password to be checked.

    Returns:
        bool: True if the password matches the hashed password, False otherwise.
    """
    # Encode the password to bytes as bcrypt expects bytes
    password_bytes = password.encode('utf-8')
    # Encode the hashed password to bytes as bcrypt expects bytes
    hashed_password_bytes = hashed_password.encode('utf-8')
    # Check the password against the hashed password
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)



import hashlib

def calculate_hash(transaction):
    hash_string = f"{transaction['transaction_id']}{transaction['sender_account_id']}{transaction['receiver_account_id']}{transaction['amount']}{transaction['transaction_type']}{transaction['description']}{transaction['created_at']}{transaction['previous_hash']}"
    return hashlib.sha256(hash_string.encode()).hexdigest()

# Example transaction data
transaction = {
    'transaction_id': 1,
    'sender_account_id': 100,
    'receiver_account_id': 200,
    'amount': 150.00,
    'transaction_type': 'debit',
    'description': 'Payment for services',
    'created_at': '2024-07-09 12:34:56',
    'previous_hash': 'previous_transaction_hash_here'
}

# # Calculate the transaction hash
# transaction_hash = calculate_hash(transaction)
# print(f"Transaction Hash: {transaction_hash}")
