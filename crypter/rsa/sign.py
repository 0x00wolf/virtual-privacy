from Crypto.Signature import pss
from Crypto.Hash import SHA3_256

from crypter.CrypterError import CrypterError


def sign(private_key, bytes_string):
    """
    Sign a message with an RSA private key.

    Args:
        private_key (RSA.RsaKey): Imported RSA private key for signing
        bytes_string (bytes): Encoded message for to be signed

    Returns:
        signature(bytestring): Signature for message authentication
    """

    try:
        h = SHA3_256.new(bytes_string)  # if string use .encode()
    except (ValueError, TypeError, AttributeError) as e:
        raise CrypterError(message=f"Error hashing bytes: {e}")
    try:
        signature = pss.new(private_key).sign(h)
    except (ValueError, TypeError, AttributeError) as e:
        raise CrypterError(message=f"Error signing message: {e}")
    else:
        return signature
