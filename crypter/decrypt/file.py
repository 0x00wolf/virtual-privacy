from Crypto.PublicKey import RSA
import json

import crypter.chacha20_poly1305.encrypt
import crypter.random_bytes
import crypter.rsa.wrap
import crypter.rsa.sign
from crypter.CrypterError import CrypterError


def file(file_in: str,
         file_out: str = None,
         private_key: RSA.RsaKey = None,
         verbose: bool = False) -> (bytes, bytes, bytes):
    """
    This function decrypts a file with the VPP.

    Args:
        file_in (str): Path to the file that will be decrypted.
        file_out (str): Path to export the decrypted file.
        private_key (RSA.RsaKey): RSA private key required to unwrap the
        session key.
        verbose (bool): Verbose printout detailing the decryption process.
    """

    try:
        with open(file_in, 'rb') as f:
            data = f.read()
    except FileNotFoundError as e:
        raise CrypterError(message=f"{e}")
    wrapped_key = data[:384]
    ciphertext = data[384:]
    session_key = crypter.rsa.unwrap(private_key=private_key,
                                     wrapped_key=wrapped_key)
    if verbose:
        print(f"[ ] Successfully unwrapped 256-bit session key.")
    unencrypted_data = crypter.chacha20_poly1305.decrypt(
        unwrapped_key=session_key,
        ciphertext=ciphertext)
    if verbose:
        print(f"[ ] Successfully decrypted data.")
    with open(file_out, 'wb') as f:
        f.write(unencrypted_data.encode())
    if verbose:
        print(f"[*] Decrypted file written to: {file_out}")