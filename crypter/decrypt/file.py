from Crypto.PublicKey import RSA

from crypter.CrypterError import CrypterError
import crypter.chacha20_poly1305
import crypter.random_bytes
import crypter.rsa


def file(file_in: str,
         file_out: str = None,
         return_context: bool = False,
         private_pem: str = None,
         private_key: RSA.RsaKey = None) -> str | None:
    """
    Opens the specified file from the path supplied and reads the wrapped key
    and ciphertext into separate variables. If the path to a PEM key has been
    provided it will import the key. Another option is to provide an RSA
    private key that has already imported for decryption. The 256-bit encrypted
    session key is unwrapped with the RSA private key and passed to a
    ChaCha20-Poly1305 stream cipher along with the ciphertext for decryption.

    If an export path has been provided the decrypted contents will be written
    to the path specified. If no export path has been provided, the plaintext
    contents will be returned as a variable. Verbose will print out detailed
    information about the decryption process.

    Args:
        file_in (str): Path to the file that is to be decrypted.
        file_out (str): Optional, specify a path to export the decrypted
        contents.
        return_context (bool): Return the plaintext as a variable.
        private_pem (str): The path to an RSA private key PEM file on disk.
        private_key (RSA.RsaKey): The receiver's RSA private key imported for
        encryption. Either a PEM or an RSA key must be supplied.

    Returns:
        plaintext: If return_context=True.

    """

    if not private_pem and not private_key:
        raise CrypterError(message=f"Error, an RSA private key is required "
                                   f"for decryption.")
    if private_pem:
        private_key = crypter.rsa.key.load_key(private_pem)
    if not file_out:
        return_context = True
    try:
        with open(file_in, 'rb') as f:
            data = f.read()
        wrapped_key = data[:384]
        ciphertext = data[384:]
    except OSError as e:
        raise CrypterError(message=f"Error importing file for "
                                   f"decryption: {e}")
    unwrapped_key = crypter.rsa.unwrap(private_key=private_key,
                                       wrapped_key=wrapped_key)
    plaintext = crypter.chacha20_poly1305.decrypt(unwrapped_key=unwrapped_key,
                                                  ciphertext=ciphertext)
    if file_out:
        try:
            with open(file_out, 'w') as f:
                f.write(plaintext)
        except IOError as e:
            raise CrypterError(message=f"Error saving decrypted file: {e}")
    if return_context:
        return plaintext
