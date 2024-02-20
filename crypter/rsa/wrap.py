from Crypto.Cipher import PKCS1_OAEP

from crypter.CrypterError import CrypterError


def wrap(public_key, bytes_string):
    """
    Uses an imported RSA public key to wrap a symmetric session key.

    Args:
        public_key (RSA.Rsa.Key): RSA public key ready for encryption
        bytes_string (bytes): Used to encrypt the 256-bit symmetric key
        used by the crypter package for AES or ChaCha20 encryption.

    Returns:
        wrapped_key (bytes): RSA wrapped session key
    """

    try:
        cipher_rsa = PKCS1_OAEP.new(public_key)
        wrapped_key = cipher_rsa.encrypt(bytes_string)
        return \
            wrapped_key
    except (ValueError, AttributeError, TypeError) as e:
        raise CrypterError(message=f'PKCS#1 OAEP cipher error: {e}')
