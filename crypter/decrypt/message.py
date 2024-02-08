from Crypto.PublicKey import RSA

from crypter.CrypterError import CrypterError
import crypter.chacha20_poly1305
import crypter.random_bytes
import crypter.rsa


def message(wrapped_key: bytes,
            file_out: str = None,
            ciphertext: str = None,
            private_pem: str = None,
            private_key: RSA.RsaKey = None) -> str | None:
    """
    Takes the wrapped key and ciphertext into separate variables. If the path
    to a PEM key has been provided it will import the key. Another option is to
    provide an RSA private key that has already imported for decryption.

    The 256-bit encrypted session key is unwrapped with the RSA private key and
    passed to a ChaCha20-Poly1305 stream cipher along with the ciphertext
    for decryption. The decrypted plaintext is returned as a variable. If
    verbose=True, detailed information about the decryption process will be
    provided.

    If a 'file_out' export path has been provided the decrypted contents will
    be written to the path specified along with being returned as a variable.

    Args:
        ciphertext (str): ChaCha20 JSON containing the ciphertext.
        wrapped_key (bytes): The RSA wrapped 256-bit decryption key.
        file_out (str): An optional path to export the plaintext.
        private_pem (str): The path to an RSA private key PEM file on disk.
        private_key (RSA.RsaKey): The receiver's RSA private key imported for
        encryption. Either a PEM or an RSA key must be supplied.

    Returns:
        plaintext (str): If successful, returns the decrypted message

    """

    if not private_pem and not private_key:
        raise CrypterError("\n[!] Error, an RSA private key is required "
                           "for decryption.")
    if private_pem:
        private_key = crypter.rsa.key.load.key(private_pem)
    unwrapped_key = crypter.rsa.unwrap(private_key=private_key,
                                       wrapped_key=wrapped_key)
    plaintext = crypter.chacha20_poly1305.decrypt(unwrapped_key=unwrapped_key,
                                                  ciphertext=ciphertext)
    if file_out:
        try:
            with open(file_out, 'w') as f:
                f.write(plaintext)
        except (ValueError, IOError) as e:
            raise CrypterError(message=f"Error saving decrypted message "
                                       f"to disk: {e}")
    return plaintext
