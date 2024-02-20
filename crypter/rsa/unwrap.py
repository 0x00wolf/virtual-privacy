from Crypto.Cipher import PKCS1_OAEP

from crypter.CrypterError import CrypterError


def unwrap(private_key, wrapped_key):
    """
    Use an RSA private key to unwrap a symmetric session key.

    Args:
        private_key (RSA.RsaKey): Imported RSA private key
        wrapped_key (bytes): RSA wrapped 256-bit session key

    Returns:
        session_key (bytes): Unwrapped session key
    """

    try:
        cipher_rsa = PKCS1_OAEP.new(private_key)
        session_key = cipher_rsa.decrypt(wrapped_key)
        return \
            session_key
    except (AttributeError, ValueError, TypeError) as e:
        raise CrypterError(message=f"PKCS#1 OAEP cipher decryption error: {e}")
