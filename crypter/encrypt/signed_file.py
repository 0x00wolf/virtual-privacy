from Crypto.PublicKey import RSA
import json

import crypter.chacha20_poly1305.encrypt
import crypter.random_bytes
import crypter.rsa.wrap
import crypter.rsa.sign
from crypter.CrypterError import CrypterError


def signed_file(file_in: str,
                file_out: str,
                public_key: RSA.RsaKey,
                private_key: RSA.RsaKey,
                verbose: bool = False) -> None:
    """
    A function to encapsulate ChaCha20-Poly1305 wrapped RSA hybrid encryption
    with signature verification. This process provides confidentiality,
    authenticity, and integrity.

    First, the function signs the file. Second, the function
    generates a 256-bit session key. Third, the function wraps the 256-bit
    session key with the RSA public key belonging to the receiver.
    Fourth, the function encrypts the UTF-8 encoded data with the session key.
    If verbose==True, the function will print out information. Finally, it
    returns the RSA wrapped key, signature, and ciphertext.

    Args:
        file_in (str): Path to the file that will be encrypted.
        file_out (str): Path to export the encrypted file.
        public_key (RSA.RsaKey): The receiver's RSA public key.
        private_key (RSA.RsaKey): The sender's RSA private key.
        verbose (bool): Print out additional information about the encryption
        process.

    """

    try:
        with open(file_in, 'rb') as f:
            data = f.read()
    except OSError as e:
        raise CrypterError(message=f"{e}")
    signature = crypter.rsa.sign(private_key=private_key,
                                 bytes_string=data)
    if verbose:
        print(f'[ ] Message successfully signed with local {private_key}.')
    session_key = crypter.random_bytes(32)
    if verbose:
        print(f'[ ] Generating random 256-bit session key.')
    session_key, ciphertext = crypter.chacha20_poly1305.encrypt(
        bytes_string=data,
        session_key=session_key)
    if verbose:
        cipher_t = json.loads(ciphertext)
        print(f"[ ] Message encrypted with session key & "
              f"ChaCha20-Poly1305 stream-cipher.")
    wrapped_key = crypter.rsa.wrap(public_key=public_key,
                                   bytes_string=session_key)
    if verbose:
        print(f"[ ] Session key successfully wrapped with RSA public key")
    try:
        with open(file_out, 'wb') as f:
            f.write(wrapped_key)
            f.write(signature)
            f.write(ciphertext.encode())
        print(f"[*] Encrypted payload written to: {file_out}")
    except OSError as e:
        raise CrypterError(message=f"Crypter error {e}")