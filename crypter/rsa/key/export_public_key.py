from Crypto.PublicKey import RSA

from crypter.CrypterError import CrypterError


def export_public_key(private_key: RSA.RsaKey, export_path: str):
    try:
        public_key = private_key.publickey().export_key()
    except (ValueError, AttributeError, TypeError) as e:
        raise CrypterError(message=f"Error exporting RSA public key: {e}")
    try:
        with open(export_path, "wb") as f:
            f.write(public_key)
    except OSError as e:
        raise CrypterError(message=f"Error writing RSA public key to "
                                   f"file: {e}")
