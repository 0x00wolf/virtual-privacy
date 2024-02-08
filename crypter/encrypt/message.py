from Crypto.PublicKey import RSA

from crypter.CrypterError import CrypterError
import crypter.chacha20_poly1305
import crypter.random_bytes
import crypter.rsa


def message(bytes_string: bytes,
            public_pem: str = None,
            public_key: RSA.RsaKey = None):
    """
    Accepts the path to an RSA public key PEM file on disk, or optionally, a
    previously imported RSA public key can be provided. The program generates
    a new 256-bit session key, which is passed to a ChaCha20-Poly1305
    stream cipher, along with the plaintext for encryption.

    If an export path has been specified, the encrypted data and the wrapped
    key are exported to the path specified, or returned as variables.
    Writing to a file and returning the wrapped key and ciphertext as
    variables is also an option pu(see the arguments below).

    Args:
        bytes_string (bytes): The target encoded message for encryption.
        public_pem (str): The path to the receiver's RSA public key PEM file.
        public_key (RSA.RsaKey): A previously imported RSA public key.

    Returns:
        wrapped_key (bytes): The RSA wrapped 256-bit session key.
        ciphertext (str): The JSON containing the ciphertext, nonce, and
        header, resulting from the ChaCha20-Poly1305 stream cipher.
    """

    if not public_key and not public_pem:
        raise CrypterError(message=f"Error, an RSA public key is "
                                   f"required for encryption.")
    if public_pem:
        public_key = crypter.rsa.key.load_key(public_pem)
    session_key = crypter.random_bytes(32)
    wrapped_key = crypter.rsa.wrap(public_key=public_key,
                                   bytes_string=session_key)
    session_key, ciphertext = crypter.chacha20_poly1305.encrypt(
        bytes_string=bytes_string,
        session_key=session_key)
    return wrapped_key, ciphertext

