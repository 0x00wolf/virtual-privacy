from crypter.CrypterError import CrypterError


def open_pem(pem_path: str):
    """
    Internal function to open the RSA PEM file and return it as a string, or
    print an error & exit if the file is not found.
    Args:
        pem_path (str): Path to the key PEM file on disk.

    Returns:
    """

    try:
        with open(pem_path, 'rb') as f:
            return f.read()
    except FileNotFoundError as e:
        raise CrypterError(message=f"Error, RSA PEM file not found: {e}")
