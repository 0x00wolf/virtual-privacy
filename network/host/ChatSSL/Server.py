import ssl
import socket
import base64
import threading
from datetime import datetime

from network.NetworkError import NetworkError
from network.vp_protocol.b64_send import b64_send
from network.vp_protocol.b64_recv import b64_recv


class Server:
    def __init__(self, host: str, port: int, banner: str, certificate: str,
                 private_pem: str):
        self.host = host
        self.port = port
        self.banner = banner
        self.connections = []
        self.private_pem = private_pem
        self.certificate = certificate

    def run(self):
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(self.certificate, self.private_pem)
        except OSError as e:
            raise NetworkError(message=f"SSL context creation error {e}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind((self.host, self.port))
            except (PermissionError, OSError) as e:
                raise NetworkError(message=f"{e}")
            sock.listen()
            with context.wrap_socket(sock, server_side=True) as ssock:
                print(f"[*] SSL encrypted Chatroom Server listening on ~ "
                      f"{self.host}:{self.port}.")
                while True:
                    try:
                        conn, addr = ssock.accept()
                    except ssl.SSLError as e:
                        print(f"[!] Client failed to connect"
                              f" {self.datestamp()}")
                        continue
                    print(f"[*] Accepted connection from "
                          f"{addr[0]}:{addr[1]} {self.datestamp()}")
                    client = threading.Thread(
                        target=self.handle_client,
                        args=(conn, addr),
                        daemon=True)
                    client.start()

    def handle_client(self, conn, addr):
        with conn:
            try:
                b64_send(message_str='Username: ', conn=conn)
                username = b64_recv(conn=conn)
                if not username:
                    raise NetworkError(
                        message=f"[!] {addr[0]}:{addr[1]} ~ Error receiving "
                                f"username, dropping connection "
                                f"{self.datestamp()}")
                else:
                    print(f"[*] {addr[0]}:{addr[1]} ~ user: "
                          f"{username} connected {self.datestamp()}")
                    b64_send(message_str=self.banner, conn=conn)
                    self.connections.append(conn)
                    self.broadcast(conn=conn, addr=addr, username=username)
                    try:
                        while True:
                            message = b64_recv(conn=conn)
                            if not message:
                                raise OSError
                            else:
                                print(f"[*] {addr[0]}:{addr[1]} ~ message "
                                      f"received {self.datestamp()}.")
                                print(f"[ ] Base64 decoded message: {message}")
                                self.broadcast(conn=conn, addr=addr,
                                               username=username,
                                               data=message)
                    except (OSError, ValueError, NetworkError) as e:
                        print(f"[!] {addr[0]}:{addr[1]} ~ disconnected "
                              f"{self.datestamp()}.")
                        self.remove_client(conn)
            except NetworkError as e:
                print(f"[!] {addr[0]}:{addr[1]} ~ Connection error, "
                      f"disconnecting {self.datestamp()}")
                self.remove_client(conn)

    def broadcast(self, conn, addr, username, data=None):
        for client in self.connections:
            if client != conn:
                try:
                    (print
                     (f"[>] broadcasting from {addr[0]}:{addr[1]} to "
                      f"{client.getpeername()[0]}:{client.getpeername()[1]} "
                      f"{self.datestamp()}."))
                    if not data:
                        b64_send(message_str=f">>> {username} connected "
                                             f"{self.datestamp()}",
                                 conn=client)
                    else:
                        b64_send(message_str=f"{username}: {data}",
                                 conn=client)
                except (OSError, NetworkError) as e:
                    print(f"[!] {addr[0]}:{addr[1]} ~ disconnected "
                          f"{self.datestamp()}.")
                    self.remove_client(conn)

    def remove_client(self, conn):
        if conn in self.connections:
            conn.close()
            self.connections.remove(conn)

    @staticmethod
    def datestamp():
        return f"@ {datetime.now().strftime('%m/%d/%Y-%H:%M:%S')}"
