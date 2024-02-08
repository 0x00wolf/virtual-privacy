from Crypto.Signature import pss
from Crypto.Hash import SHA3_256

from crypter.CrypterError import CrypterError


def verify(public_key, signature, bytes_string):
    """
    Verify a signature with the corresponding RSA public key.

    Args:
        public_key (RSA.RsaKey): RSA public key for signature verification
        signature (bytes): Signature that needs to be verified
        bytes_string (bytes): Encoded message for hashing.

    Returns:
        True or False (bool): True if good signature.
    """

    h = SHA3_256.new(bytes_string)
    verifier = pss.new(public_key)
    try:
        verifier.verify(h, signature)
        return True, h
    except (ValueError, TypeError, AttributeError) as e:
        raise CrypterError(message=f"Error validating RSA signature: {e}")
