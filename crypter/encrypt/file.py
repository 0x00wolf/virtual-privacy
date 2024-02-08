from Crypto.PublicKey import RSA

import crypter.chacha20_poly1305
import crypter.random_bytes
import crypter.rsa


def file(file_in: str,
         file_out: str = None,
         return_context: bool = False,
         public_pem: str = None,
         public_key: RSA.RsaKey = None):
    """
    Opens the specified file from the path supplied and reads the contents
    into a variable. Generates a new 256-bit session key, which is passed to a
    ChaCha20-Poly1305 stream cipher, which encrypts the file's contents.

    Then, if a file out path has been specified, the encrypted data and the wrapped
    key are exported to the path specified, or returned as variables. Writing
    to a file and returning the wrapped key and ciphertext as variables is
    also an option (see the arguments below).

    Required: Either an RSA public key previously imported, or the path to an
    RSA public key PEM file on disk.

    Args:
       file_in (str): Path to the file that is to be encrypted.
       file_out (str): Optional, an export path.
       return_context (bool): Return the wrapped key & ciphertext as vars.
       public_pem (str): The path to an RSA public key PEM file on disk.
       public_key (RSA.RsaKey): The receiver's RSA public key imported

    Returns:
       wrapped_key (bytes): If return_context=True.
       ciphertext (bytes): If return_context=True.
    """

    if not public_pem and not public_pem:
        raise CrypterError(message=f"Error, an RSA public key is required "
                                   f"for encryption.")
    if public_pem:
        public_key = crypter.rsa.key.load_key(public_pem)
    if not file_out:
        return_context = True
    try:
        with open(file_in, 'rb') as f:
            plaintext = f.read()
            print(f"\n[ ] Encrypting: {file_in}")
    except FileNotFoundError as e:
        raise CrypterError(message=f"Error, file not found: {e}")
    session_key = crypter.random_bytes(32)
    wrapped_key = crypter.rsa.wrap(public_key=public_key,
                                   bytes_string=session_key)
    session_key, ciphertext = crypter.chacha20_poly1305.encrypt(
        bytes_string=plaintext,
        session_key=session_key)
    if file_out:
        try:
            with open(file_out, 'wb') as f:
                f.write(wrapped_key)
                f.write(ciphertext.encode())
        except OSError as e:
            raise CrypterError(message=f"Error writing encrypted file: {e}")
    if return_context:
        return wrapped_key, ciphertext
