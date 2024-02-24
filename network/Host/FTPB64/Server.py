import base64
import socket
import threading
from datetime import datetime

from network.NetworkError import NetworkError


class Server:
    def __init__(self, host: str, port: int, file_in: str):
        self.host = host
        self.port = port
        self.file_in = file_in

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind((self.host, self.port))
            except (PermissionError, OSError) as e:
                raise NetworkError(message=f"{e}")
            sock.listen()
            print(f"[*] Base64 encoded FTP Server listening on "
                  f"{self.host}:{self.port}")
            while True:
                try:
                    conn, addr = sock.accept()
                except ConnectionError as e:
                    print(f"[!] Client error connecting {self.datestamp()}")
                    continue
                print(f"[*] {addr[0]}:{addr[1]} ~ Connected "
                      f"{self.datestamp()}")
                client = threading.Thread(
                    target=self.handle_client,
                    args=(conn, addr))
                client.start()

    def handle_client(self, conn, addr):
        print(f"[*] {addr[0]}:{addr[1]} ~ Commencing download "
              f"{self.datestamp()}")
        try:
            total_bytes = 0
            f = open(self.file_in, 'rb')
            while True:
                buffer = f.read(1024)
                while buffer:
                    try:
                        total_bytes += len(buffer)
                        conn.send(base64.b64encode(buffer))
                    except OSError as e:
                        raise NetworkError(message=f"{e}")
                    buffer = f.read(1024)
                if not buffer:
                    f.close()
                    conn.close()
                    print(f"[*] {addr[0]}:{addr[1]} ~ File transfer successful"
                          f" {self.datestamp()}")
                    print(f'[ ] Total bytes transferred: {total_bytes}')
                    break
        except NetworkError as e:
            print(f"[!] {addr[0]}:{addr[1]} ~ Connection error {e} "
                  f"{self.datestamp()}")
            return

    @staticmethod
    def datestamp():
        return f"@ {datetime.now().strftime('%m/%d/%Y-%H:%M:%S')}"