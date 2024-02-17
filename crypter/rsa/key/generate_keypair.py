from Crypto.PublicKey import RSA

from crypter.CrypterError import CrypterError


def generate_keypair(private_key_file_out, public_key_file_out, password=None):
    """
    A function that generates a new RSA keypair. If a string password is
    supplied, the function will use it to encrypt the RSA private key.

    Args:
        private_key_file_out (str): The path to export the RSA private key.
        public_key_file_out (str): The path to export the RSA public key.
        password (str): Use a password? True or False.

    Returns:
        None (None): If successful saves key pair to disk as PEM files.
    """

    try:
        private_key = RSA.generate(3072)
    except (ValueError, AttributeError, TypeError) as e:
        raise CrypterError(message=f"Error generating RSA private key: {e}")
    try:
        public_key = private_key.publickey().export_key()
    except (ValueError, AttributeError, TypeError) as e:
        raise CrypterError(message=f"Error exporting RSA public key: {e}")
    try:
        with open(public_key_file_out, "wb") as f:
            f.write(public_key)
    except OSError as e:
        raise CrypterError(message=f"Error writing RSA public key to "
                                   f"file: {e}")
    try:
        if password:
            data = private_key.export_key(
                format='PEM',  # PEM, DER, or OpenSSH
                passphrase=password,
                pkcs=8,  # See Pycryptodome derivatives
                protection='PBKDF2WithHMAC-SHA512AndAES256-CBC',
                prot_params={'iteration_count': 131072})
        else:
            data = private_key.export_key(format='PEM',)
    except (ValueError, IndexError, TypeError) as e:
        raise CrypterError(message=f"Error exporting RSA private key: {e}")
    try:
        with open(private_key_file_out, 'wb') as f:
            f.write(data)
        print(f"\n[*] Saving private key to: "
              f"'{private_key_file_out}'"
              f"\n[*] Saving public key to: "
              f"'{public_key_file_out}'")
    except (ValueError, IndexError, TypeError, OSError) as e:
        raise CrypterError(message=f"Error writing RSA private key to "
                                   f"file: {e}")
