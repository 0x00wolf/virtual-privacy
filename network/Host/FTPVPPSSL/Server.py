import ssl
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
                 private_pem: str,
                 certificate: str,
                 database_path: str):
        self.host = host
        self.port = port
        self.file_in = file_in
        self.private_key = private_key
        self.private_pem = private_pem
        self.certificate = certificate
        self.database_path = database_path

    def run(self):
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(certfile=self.certificate,
                                    keyfile=self.private_pem)
            print(f"[*] SSL context loaded")
        except OSError as e:
            raise NetworkError(message=f"[!] SSL context creation error {e}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind((self.host, self.port))
                sock.listen()
            except (PermissionError, OSError) as e:
                raise NetworkError(message=f"{e}")
            with context.wrap_socket(sock, server_side=True) as ssock:
                print(f"[*] VPP wrapped in SSL encrypted FTP Server listening "
                      f"on ~ "
                      f"{self.host}:{self.port} {self.datestamp()}")
                try:
                    while True:
                        try:
                            conn, addr = ssock.accept()
                        except (ssl.SSLError, ConnectionError) as e:
                            continue
                        print(f"[*] {addr[0]}:{addr[1]} ~ Connected, starting "
                              f"authentication process {self.datestamp()}")
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

    def handle_client(self, conn, addr, public_key):
        print(f"[*] {addr[0]}:{addr[1]} ~ Commencing download "
              f"{self.datestamp()}")
        f = open(self.file_in, 'rb')
        try:
            while True:
                buffer = f.read(1024)
                while buffer:
                    try:
                        vp_send(message=buffer.decode(),
                                conn=conn,
                                private_key=self.private_key,
                                public_key=public_key,
                                verbose=True)
                    except OSError as e:
                        raise NetworkError(message=f"{e}")
                    buffer = f.read(1024)
                if not buffer:
                    f.close()
                    conn.close()
                    print(f"[*] {addr[0]}:{addr[1]} ~ File transfer successful "
                          f"{self.datestamp()}")
                    break
        except NetworkError as e:
            print(f"[!] {addr[0]}:{addr[1]} ~ Transmission error "
                  f"{self.datestamp()}")
            conn.close()

    @staticmethod
    def datestamp():
        return f"@ {datetime.now().strftime('%m/%d/%Y-%H:%M:%S')}"