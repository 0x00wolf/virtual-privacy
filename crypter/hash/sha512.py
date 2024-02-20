import hashlib


def sha512(byte_string: bytes) -> str:
    """
    Returns a SHA512 Hash hex digest.

    Args:
        byte_string:

    Returns:
        h (str): hexdigest

    """

    try:
        h = hashlib.sha512(byte_string)
    except TypeError as e:
        print(f'\n[!] Error creating hash: {e}')
        raise CrypterError
    return h.hexdigest()
