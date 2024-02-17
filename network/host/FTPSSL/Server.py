import ssl
import base64
import socket
import threading
from datetime import datetime

from network.NetworkError import NetworkError


class Server:
    def __init__(self, host: str, port: int, file_in: str, private_pem: str,
                 certificate: str):
        self.host = host
        self.port = port
        self.file_in = file_in
        self.private_pem = private_pem
        self.certificate = certificate

    def run(self):
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(self.certificate, self.private_pem)
            print(f"[*] SSL context loaded")
        except OSError as e:
            raise NetworkError(message=f"[!] SSL context creation error {e}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind((self.host, self.port))
            except (PermissionError, OSError) as e:
                raise NetworkError(message=f"{e}")
            sock.listen()
            with context.wrap_socket(sock, server_side=True) as ssock:
                print(f"[*] SSL encrypted FTP Server listening on ~ "
                      f"{self.host}:{self.port} {self.datestamp()}")
                while True:
                    try:
                        conn, addr = ssock.accept()
                    except ssl.SSLError as e:
                        continue
                    client = threading.Thread(
                        target=self.handle_client,
                        args=(conn, addr))
                    client.start()

    def handle_client(self, conn, addr):
        try:
            print(f"[*] {addr[0]}:{addr[1]} ~ Commencing download "
                  f"{self.datestamp()}")
            try:
                f = open(self.file_in, 'rb')
            except FileNotFoundError as e:
                raise NetworkError(message=f"{e}")
            while True:
                buffer = f.read(1024)
                while buffer:
                    conn.send(base64.b64encode(buffer))
                    buffer = f.read(1024)
                if not buffer:
                    f.close()
                    conn.close()
                    print(f"[*] {addr[0]}:{addr[1]} ~ File transfer successful "
                          f"{self.datestamp()}")
                    break
        except NetworkError as e:
            print(f"[!] {addr[0]}:{addr[1]} ~ Connection error {e}")
            conn.close()
            return

    @staticmethod
    def datestamp():
        return f"@ {datetime.now().strftime('%m/%d/%Y-%H:%M:%S')}"