import sys

import crypter.rsa.key.load_key
from crypter.CrypterError import CrypterError


def load_keys(private_pem, public_pem, password=None):
    """
    Imports an RSA key pair (public & private key), ready for encryption
    & decryption. Also handles decrypting password protected RSA private keys
    files when supplied with a password.

    Args:
        private_pem (str): Path to an RSA private key PEM file.
        public_pem (str): Path to an RSA public key PEM file.
        password (str): Password to decrypt an RSA private key.

    Returns:
        private_key (RSA.RsaKey)
        public_key (RSA.RsaKey)
    """
    private_key = crypter.rsa.key.load_key(pem_path=private_pem,
                                           password=password)
    public_key = crypter.rsa.key.load_key(pem_path=public_pem)
    return private_key, public_key

