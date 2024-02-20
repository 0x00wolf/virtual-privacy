import hashlib


def sha256(byte_string: bytes):
    """
    Returns the hex digest of a SHA256 hash (courtesy of hashlib).

    Args:
        byte_string (bytes): The 'utf-8' encoded string to be hashed.

    Returns:
        hex_string (str): Hex digest of the s
    """

    try:
        h = hashlib.sha256(byte_string)
    except TypeError as e:
        print(f'\n[!] Error creating hash: {e}')
        raise CrypterError
    return h.hexdigest()
