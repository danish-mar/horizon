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