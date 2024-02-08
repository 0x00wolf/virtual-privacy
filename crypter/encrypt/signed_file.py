from Crypto.PublicKey import RSA

import crypter.chacha20_poly1305
import crypter.random_bytes
import crypter.rsa


def signed_file(file_in: str,
                file_out: str = None,
                return_context: bool = False,
                public_pem: str = None,
                public_key: RSA.RsaKey = None,
                private_pem: str = None,
                private_key: RSA.RsaKey = None,
                password: str = None):
    """
    Opens the specified file from the path supplied and reads the contents
    into a variable. Generates a new 256-bit session key, which is passed to a
    ChaCha20-Poly1305 stream cipher, which encrypts the file's contents.

    Then, if a file out path has been specified, the encrypted data and the wrapped
    key are exported to the path specified, or returned as variables. Writing
    to a file and returning the wrapped key and ciphertext as variables is
    also an option (see the arguments below).

    Optional: This function requires the RSA private key of the sender, and
    the RSA public key of the receiver. You can provide the path to a PEM
    file on disk or an imported key for either the public or private key. The
    only requirement is that one of each is passed for both keys.

    Args:
       file_in (str): Path to the file that is to be encrypted.
       file_out (str): Optional, an export path.
       return_context (bool): Return the wrapped key & ciphertext as vars.
       public_pem (str): The path to an RSA public key PEM file on disk.
       private_pem (str): The path to an RSA private key PEM file on disk.
       password (str): The password for the sender's RSA private key (if
       required).
       public_key (RSA.RsaKey): The receiver's RSA public key imported for
       encrypting the 256-bit session key.
       private_key (RSA.RsaKey): The sender's RSA private key imported for
       signing.
       verbose (bool): Print out verbose information about the process.

    Returns:
       wrapped_key (bytes): If return_context=True.
       signature (bytes): The sender's RSA signature from the file.
       ciphertext (bytes): If return_context=True.
    """

    if not public_pem and not public_key:
        raise CrypterError(message=f"\n[!] Error, an RSA public key is "
                                   f"required for encryption.")
    if public_pem:
        public_key = crypter.rsa.key.load_key(public_pem)
    if not private_pem and not private_key:
        raise CrypterError(message=f"Error, an RSA private key is "
                                   f"required for encryption.")
    if private_pem:
        private_key = crypter.rsa.key.load_key(private_pem)
    if not file_out:
        return_context = True
    try:
        with open(file_in, 'rb') as f:
            bytes_string = f.read()
            print(f"\n[ ] Encrypting: {file_in}")
    except FileNotFoundError as e:
        raise CrypterError(message=f"Error, file not found: {e}")
    signature = crypter.rsa.sign(private_key=private_key,
                                 bytes_string=bytes_string)
    session_key = crypter.random_bytes(32)
    wrapped_key = crypter.rsa.wrap(public_key=public_key,
                                   bytes_string=session_key)
    session_key, ciphertext = crypter.chacha20_poly1305.encrypt(
        bytes_string=plaintext,
        session_key=session_key)
    file_out = './encrypted.bin'
    if file_out:
        try:
            with open(file_out, 'wb') as f:
                f.write(wrapped_key)
                f.write(ciphertext.encode())
        except OSError as e:
            raise CrypterError(message=f"Error writing encrypted file: {e}")
    if return_context:
        return wrapped_key, ciphertext
