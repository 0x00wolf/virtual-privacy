import socket
from Crypto.PublicKey import RSA
import crypter.rsa.key.load_key


class Connection:
    """
    A class to model a client connection to a server
    """

    def __init__(self, conn: socket.socket,
                 addr: tuple,
                 username: str,
                 public_key: RSA.RsaKey) -> None:
        self.conn = conn
        self.addr = addr
        self.username = username
        self.public_key = public_key
