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