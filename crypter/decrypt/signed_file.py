from Crypto.PublicKey import RSA
import json

import crypter.chacha20_poly1305.encrypt
import crypter.random_bytes
import crypter.rsa.wrap
import crypter.rsa.sign
from crypter.CrypterError import CrypterError


def signed_file(file_in: str,
                file_out: str = None,
                public_key: RSA.RsaKey = None,
                private_key: RSA.RsaKey = None,
                verbose: bool = False) -> (bytes, bytes, bytes):
    """
    This function decrypts a file and verifies the senders signature. The
    function fails if the incorrect public key is provided for signature
    verification.

    Args:
        file_in (str): Path to the file that will be decrypted.
        file_out (str): Path to export the decrypted file.
        public_key (RSA.RsaKey): RSA public key to verify the file's signature.
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
    signature = data[384:768]
    ciphertext = data[768:]
    session_key = crypter.rsa.unwrap(private_key=private_key,
                                     wrapped_key=wrapped_key)
    if verbose:
        print(f"[ ] Successfully unwrapped 256-bit session key.")
    unencrypted_data = crypter.chacha20_poly1305.decrypt(
        unwrapped_key=session_key,
        ciphertext=ciphertext.decode()
    )
    if verbose:
        print(f"[ ] Successfully decrypted data.")
    crypter.rsa.verify(public_key=public_key,
                       signature=signature,
                       bytes_string=unencrypted_data.encode())
    with open(file_out, 'wb') as f:
        f.write(unencrypted_data.encode())
    if verbose:
        print(f"[*] Decrypted file written to: {file_out}")