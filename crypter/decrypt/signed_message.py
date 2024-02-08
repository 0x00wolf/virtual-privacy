from Crypto.PublicKey import RSA

from crypter.CrypterError import CrypterError
import crypter.chacha20_poly1305
import crypter.rsa


def signed_message(private_key: RSA.RsaKey,
                   public_key: RSA.RsaKey,
                   wrapped_key: bytes,
                   signature: bytes,
                   ciphertext: str,
                   verbose: bool = False):
    """
       Takes the wrapped key and ciphertext into separate variables. If the
       path to a PEM key has been provided it will import the key. Another
       option is to provide an RSA private key that has already imported for
       decryption.

       The 256-bit encrypted session key is unwrapped with the RSA private key
       and passed to a ChaCha20-Poly1305 stream cipher along with the
       ciphertext for decryption. The decrypted plaintext is returned as a
       variable. If verbose=True, detailed information about the decryption
       process will be provided.

       If a 'file_out' export path has been provided the decrypted contents
       will be written to the path specified along with being returned as a
       variable.

       Args:
           wrapped_key (bytes): The RSA wrapped 256-bit decryption key.
           signature (bytes): The bytes comprising the sender's signature of
           the message's SHA256 hash.
           ciphertext (str): ChaCha20 JSON containing the ciphertext.
           private_key (RSA.RsaKey): The receiver's RSA private key imported
           for encryption. Either a PEM or an RSA key must be supplied.
           public_key (RSA.RsaKey): The sender's RSA public key for signature
           verification.
           verbose (bool): Print out verbose information about the decryption
           process.

       Returns:
           plaintext(str): The decrypted ciphertext message.

    """

    unwrapped_key = crypter.rsa.unwrap(private_key=private_key,
                                       wrapped_key=wrapped_key)
    if verbose:
        print(f"[ ] Successfully unwrapped session key. First 10 bytes: "
              f"{unwrapped_key[:10]}")
    plaintext = crypter.chacha20_poly1305.decrypt(
        unwrapped_key=unwrapped_key,
        ciphertext=ciphertext)
    if verbose:
        print(f"[ ] Successfully decrypted message: {plaintext}")
    good_signature, message_hash = crypter.rsa.verify(
        public_key=public_key,
        signature=signature,
        bytes_string=plaintext.encode())
    if verbose:
        print(f"[ ] Signature verified signature with sender's {public_key}")
    return plaintext

