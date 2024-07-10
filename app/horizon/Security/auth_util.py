import secrets
import base64

def generate_auth_key(length=32):
    """
    Generates a secure and random auth key of specified length.

    Args:
        length (int, optional): Length of the auth key in bytes. Defaults to 32.

    Returns:
        str: The generated auth key encoded as a base64 string.
    """
    # Generate random bytes using secrets module for cryptography
    random_bytes = secrets.token_bytes(nbytes=length)
    # Encode the random bytes to base64 string for easier storage and usage
    auth_key = base64.urlsafe_b64encode(random_bytes).decode('utf-8')
    return auth_key






