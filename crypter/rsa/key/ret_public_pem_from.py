from Crypto.PublicKey import RSA


def ret_public_pem_from(private_key) -> bytes:
    """
    Function to return an encoded RSA public key pem bytes string from an
    imported RSA private key.

    Args:
        private_key: The imported RSA public key.

    Returns:
        bytes: The RSA public key pem bytes string.
    """
    public_key = private_key.public_key().export_key(format='PEM')
    return public_key

