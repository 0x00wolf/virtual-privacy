from Crypto.Hash import SHA3_256


def sha3_256(byte_string):
    """
    Returns a hex digest of a SHA3-256 hash.

    Args:
        byte_string (bytestring): UTF-8 encoded string for hashing

    Returns:
        sha2_hex (str): Hex-digest of sha2_256 hash
    """

    try:
        sha3_hex = SHA3_256.new(byte_string).hexdigest()
    except TypeError as e:
        raise CrypterError(message=f'Error creating hash: {e}')
    return sha3_hex
