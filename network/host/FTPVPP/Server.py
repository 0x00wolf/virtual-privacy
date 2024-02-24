import base64
import socket
import threading
from datetime import datetime

from Crypto.PublicKey import RSA

from network.NetworkError import NetworkError
from network.vp_protocol.vp_recv import vp_recv
from network.vp_protocol.vp_send import vp_send
from network.vp_protocol.authentication.server import server as vp_server_auth


class Server:
    def __init__(self,
                 host: str,
                 port: int,
                 file_in: str,
                 private_key: RSA.RsaKey,
                 database_path: str):
        self.host = host
        self.port = port
        self.file_in = file_in
        self.private_key = private_key
        self.database_path = database_path

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind((self.host, self.port))
            except (PermissionError, OSError) as e:
                raise NetworkError(message=f"{e}")
            sock.listen(5)
            print(f"[*] VP protocol encrypted FTP Server listening on "
                  f"{self.host}:{self.port}")
            while True:
                try:
                    conn, addr = sock.accept()
                except ConnectionError as e:
                    print(f"[!] Client connection error "
                          f"{self.datestamp()}")
                    continue
                print(f"[*] {addr[0]}:{addr[1]} ~ Connected, starting "
                      f"authentication process {self.datestamp()}")
                try:
                    public_key = vp_server_auth(
                        conn=conn,
                        addr=addr,
                        private_key=self.private_key,
                        database_path=self.database_path)
                    client = threading.Thread(
                        target=self.handle_client,
                        args=(conn, addr, public_key))
                    client.start()
                except NetworkError as e:
                    print(f"[!] {addr[0]}:{addr[1]} ~ Connection error, "
                          f"disconnecting {self.datestamp()}")
                    continue

    def handle_client(self, conn, addr, public_key):
        print(f"[*] {addr[0]}:{addr[1]} ~ Commencing download "
              f"{self.datestamp()}")
        f = open(self.file_in, 'r')
        try:
            while True:
                buffer = f.read(4096)
                while buffer:
                    try:
                        vp_send(conn=conn,
                                message=buffer,
                                private_key=self.private_key,
                                public_key=public_key,
                                verbose=True)
                        buffer = f.read(4096)
                    except OSError as e:
                        raise NetworkError(message=f"{e}")
                if not buffer:
                    f.close()
                    conn.close()
                    print(f"[*] {addr[0]}:{addr[1]} ~ File transfer successful"
                          f" {self.datestamp()}")
                    break
        except NetworkError as e:
            print(f"[!] {addr[0]}:{addr[1]} ~ Error receiving transmission "
                  f"{self.datestamp()}")
            conn.close()

    @staticmethod
    def datestamp():
        return f"@ {datetime.now().strftime('%m/%d/%Y-%H:%M:%S')}"
