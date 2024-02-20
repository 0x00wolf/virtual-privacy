from Crypto.Hash import SHA256


def sha2_256(byte_string):
    """
    Returns a hex digest of a SHA2-256 hash.

    Args:
        byte_string (bytestring): UTF-8 encoded string for hashing

    Returns:
        sha2_hex (str): hexdigest() of the sha2_256 hash
    """

    try:
        sha2_hex = SHA256.new(byte_string).hexdigest()
    except TypeError as e:
        raise CrypterError(message=f'Error creating hash: {e}')
    return sha2_hex
