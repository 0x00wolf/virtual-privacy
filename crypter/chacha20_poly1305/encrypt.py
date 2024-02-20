from Crypto.Cipher import ChaCha20_Poly1305
from Crypto.Random import get_random_bytes
from base64 import b64encode
import json

from crypter.CrypterError import CrypterError
import crypter.rsa.wrap


def encrypt(bytes_string, session_key=None):
    """
    Generates a 256-bit session key & uses it to encrypt the plaintext with
    a ChaCha20-Poly1305 stream-cipher.

    Args:
        bytes_string (bytes): Plaintext that will be encrypted
        session_key (bytes): Optional, supply a random key for encrypting.
        Reuse of keys is not advised.

    Returns:
        result (str): JSON dict containing Base64 encoded ciphertext
        session_key (bytestring): Optional, if a session key wasn't provided,
        the function generates a 256-bit session key to encrypt the plaintext,
        which it will then return.
    """

    try:
        header = b"header"
        if not session_key:
            session_key = get_random_bytes(32)
        cipher = ChaCha20_Poly1305.new(key=session_key)
        cipher.update(header)
        ciphertext, tag = cipher.encrypt_and_digest(bytes_string)
        jk = ["nonce", "header", "ciphertext", "tag"]
        jv = [b64encode(x).decode('utf-8') for x in (cipher.nonce, header,
                                                     ciphertext, tag)]
        cipher_text = json.dumps(dict(zip(jk, jv)))
        return session_key, cipher_text
    except (ValueError, TypeError, UnicodeDecodeError) as msg:
        raise CrypterError(message=f"Error ChaCha20-Poly1305 encryption "
                                   f"failed: {msg}")
