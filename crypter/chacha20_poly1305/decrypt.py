from Crypto.Cipher import ChaCha20_Poly1305
from base64 import b64decode
import json

from crypter.CrypterError import CrypterError


def decrypt(unwrapped_key, ciphertext):
    """
    Using a ChaCha20-Poly1305 stream-cipher, decrypt the JSON encoded
    ciphertext with the unwrapped 256-bit session key.

    Args:
        unwrapped_key: The 256-bit key used to encrypt the msg
        ciphertext: Base64 encoded ciphertext in JSON format

    Returns:
        plaintext (str): The decrypted message
    """

    try:
        b64 = json.loads(ciphertext)
        jk = ["nonce", "header", "ciphertext", "tag"]
        jv = {k: b64decode(b64[k]) for k in jk}
        cipher = ChaCha20_Poly1305.new(
            key=unwrapped_key,
            nonce=jv['nonce'])
        cipher.update(jv['header'])
        plaintext = cipher.decrypt_and_verify(jv['ciphertext'],
                                              jv['tag'])
        return plaintext.decode('utf-8')
    except (ValueError, TypeError, UnicodeError) as msg:
        raise CrypterError(message=f"Error ChaCha20-Poly1305 encryption "
                                   f"failed: {msg}")
