from Crypto.PublicKey import RSA

from crypter.CrypterError import CrypterError
from crypter.rsa.key.open_pem import open_pem


def load_key(pem_path: str = None,
             pem_string: str = None,
             password=None
             ) -> RSA.RsaKey | None:
    """
    Imports an RSA key saved to disk & returns the key, ready for encryption
    or decryption.

    Args:
        pem_path (str): Relative or absolute path to an RSA key PEM file.
        pem_string (str): A key PEM as a string in-memory.
        password (str): If the user has supplied a password, it will be used
        to decrypt the RSA private key.

    Returns:
        rsa_key (RSA.RsaKey): An RSA key imported for use in a cipher.
    """

    if not pem_path and not pem_string:
        raise CrypterError(message="Error, an RSA key has not been provided.")
    if pem_path:
        pem_string = open_pem(pem_path)
    try:
        rsa_key = RSA.import_key(pem_string, passphrase=password)
        return rsa_key
    except (ValueError, IndexError, TypeError) as e:
        raise CrypterError(message=f"Error loading RSA key: {e}")
