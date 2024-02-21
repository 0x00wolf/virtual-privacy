from Crypto.Random import get_random_bytes


def random_bytes(integer: int):
    """
    Get random bytes to generate a new string of random bytes, of integer
    bytes in length.

    Args:
        integer (int): The number of bytes to generate
                        (256 for ChaCha20-Poly1305).

    Returns:
        byte_string (bytes): A random byte string of the supplied length.
    """

    return get_random_bytes(integer)

