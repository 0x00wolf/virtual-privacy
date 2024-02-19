from Crypto.PublicKey import RSA
import json

import crypter.chacha20_poly1305.encrypt
import crypter.random_bytes
import crypter.rsa.wrap
import crypter.rsa.sign
from crypter.CrypterError import CrypterError


def signed_message(encoded_string: bytes, public_key: RSA.RsaKey = None,
                   private_key: RSA.RsaKey = None, receiver: str = None,
                   verbose: bool = False) -> (bytes, bytes, bytes):
    """
    A function to encapsulate ChaCha20-Poly1305 wrapped RSA hybrid encryption
    with signature verification. This process provides confidentiality,
    authenticity, and integrity.

    First, the function signs the encoded message or data. Second, the function
    generates a 256-bit session key. Third, the function wraps the 256-bit
    session key with the RSA public key belonging to the receiver.
    Fourth, the function encrypts the UTF-8 encoded data with the session key.
    If verbose==True, the function will print out information. Finally, it
    returns the RSA wrapped key, signature, and ciphertext.

    Args:
        receiver (str): The message's receiver for verbose server output.
        encoded_string (bytes): The encoded message.
        public_key (RSA.RsaKey): The receiver's RSA public key.
        private_key (RSA.RsaKey): The sender's RSA private key.
        verbose (bool): Print out additional information about the encryption
        process.

    Returns:
        wrapped_key (bytes): The 256-bit session key encrypted with the
        receiver's RSA public key.
        signature (bytes): The message signature created with the sender's RSA
        private key.
        ciphertext (str): The JSON result from the ChaCha20-Poly1305 encryption
        process.

    """

    receiver = f"<{receiver}>'s" if receiver else "receiver's"
    signature = crypter.rsa.sign(private_key=private_key,
                                 bytes_string=encoded_string)
    if verbose:
        print(f'[ ] Message successfully signed with local {private_key}.')
    session_key = crypter.random_bytes(32)
    if verbose:
        print(f'[ ] Generating random 256-bit session key. '
              f'\n[ ] First 8 bytes of session key: '
              f'{session_key[:8]}')
    session_key, ciphertext = crypter.chacha20_poly1305.encrypt(
        bytes_string=encoded_string,
        session_key=session_key)
    if verbose:
        cipher_t = json.loads(ciphertext)
        print(f"[ ] Message encrypted with session key & "
              f"ChaCha20-Poly1305 stream-cipher."
              f"\n[ ] Ciphertext (32 bytes): {cipher_t['ciphertext'][:32]}")
    wrapped_key = crypter.rsa.wrap(public_key=public_key,
                                   bytes_string=session_key)
    if verbose:
        print(f"[ ] Session key successfully wrapped with"
              f" {receiver} RSA public key"
              f"\n[ ] First 8 bytes of wrapped key: {wrapped_key[:8]}")
    return wrapped_key, signature, ciphertext
