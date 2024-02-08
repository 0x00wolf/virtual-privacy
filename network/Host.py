from Crypto.PublicKey import RSA
from datetime import datetime
import readline
import getpass
import socket


class Host:
    """
    All Clients and Servers inherit the Host parent class.
    """

    def __init__(self,
                 host: str,
                 port: int,
                 private_key: RSA.RsaKey = None,
                 public_key: RSA.RsaKey = None,
                 certificate: str = None,
                 file_in: str = None,
                 file_out: str = None,
                 banner: str = None,
                 database_path: str = None
                 ) -> None:
        self.host = host
        self.port = port
        self.private_key = private_key
        self.public_key = public_key  # for client only (server's public key)
        self.certificate = certificate  # for TLS
        self.connections: list = []  # server only
        self.file_in = file_in
        self.file_out = file_out
        self.banner = banner  # server only
        self.database_path = database_path  # server only
        self.buffer = {'KEY': 384,
                       'SIG': 384,
                       'SML': 256,
                       'MED': 1024,
                       'LRG': 4096}

    def run(self):
        pass

    @staticmethod
    def datestamp():
        return f"@ {datetime.now().strftime('%m/%d/%Y-%H:%M:%S')}"

    @staticmethod
    def input_with_history(prompt):
        line = input(prompt)
        readline.add_history(line)
        return line

    @staticmethod
    def password_with_header(prompt):
        line = getpass.getpass(prompt)
        readline.add_history(line)
        return line

    @staticmethod
    def otp_input(prompt, max_length):
        def hook():
            readline.insert_text = lambda text: readline.insert_text(
                text[:max_length])
        readline.set_pre_input_hook(hook)
        return input(prompt)

    @staticmethod
    def throw_decoy(conn):
        """
        A function that sends a decoy HTTP response to someone trying
        to connect to a socket server with a web browser, or to a client
        that fails to connect. b'Rick Rolled...'

        Args:
            conn (socket.socket) : The client connection

        """

        decoy = b"""HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html><body><center><iframe width="560" height="315" src="https://www.youtube.com/embed/dQw4w9WgXcQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe></center></body></html>"""
        conn.sendall(decoy)
