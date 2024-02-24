import ssl
import socket
import threading
from datetime import datetime

from Crypto.PublicKey import RSA

import crypter
from network.Connection import Connection
from network.NetworkError import NetworkError
from network.vp_protocol.vp_send import vp_send
from network.vp_protocol.vp_recv import vp_recv
from network.vp_protocol.authentication.chat_server import (chat_server as
                                                            authentication)


class Server:
    def __init__(self,
                 host: str,
                 port: int,
                 banner: str,
                 private_key: RSA.RsaKey,
                 database_path: str,
                 certificate: str,
                 private_pem: str):
        self.host = host
        self.port = port
        self.private_key = private_key
        self.database_path = database_path
        self.certificate = certificate
        self.private_pem = private_pem
        self.connections = []
        self.banner = banner

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
                print(f"[*] VPP wrapped in SSL encrypted Chatroom Server listening "
                      f"on ~"
                      f" {self.host}:{self.port}.")
                while True:
                    try:
                        conn, addr = ssock.accept()
                        print(
                            f"\n[*] {addr[0]}:{addr[1]} ~ Connecting, "
                            f"commencing authentication process "
                            f"{self.datestamp()}")
                    except (OSError, ConnectionError):
                        print(f"\n[!] Connection error, dropping client "
                              f"{self.datestamp()}")
                        continue
                    try:
                        username, public_key = authentication(
                            private_key=self.private_key,
                            database_path=self.database_path,
                            conn=conn,
                            addr=addr,
                            connections=self.connections,
                            banner=self.banner,
                            verbose=True)
                    except NetworkError as e:
                        print(
                            f"\n[!] {addr[0]}:{addr[1]} ~ "
                            f"Authentication failed: {e}")
                        conn.close()
                        continue
                    new_connection = Connection(conn=conn,
                                                addr=addr,
                                                username=username,
                                                public_key=public_key)
                    self.connections.append(new_connection)
                    try:
                        client = threading.Thread(
                            target=self.handle_client,
                            args=(new_connection,),
                            daemon=True)
                        client.start()
                    except threading.ThreadError:
                        self.remove_client(new_connection)

    def handle_client(self, connection):
        with connection.conn:
            self.broadcast(connection)
            while True:
                try:
                    message = vp_recv(
                        conn=connection.conn,
                        public_key=connection.public_key,
                        private_key=self.private_key,
                        verbose=True)
                    if not message:
                        raise NetworkError
                    else:
                        self.broadcast(connection=connection,
                                       data=message)
                except (NetworkError, crypter.CrypterError) as e:
                    print(f"\n[*] {connection.addr[0]}:{connection.addr[1]} ~ "
                          f"Connection error: {e} {self.datestamp()}")
                    self.remove_client(connection=connection)
                    break

    def broadcast(self, connection, data=None):
        for client in self.connections:
            if client.conn != connection.conn:
                if not data:
                    message = (f"{connection.username} connected "
                               f"{self.datestamp()}")
                else:
                    message = f"{connection.username}: {data}"
                try:
                    print(f"\n[*] {client.addr[0]}:{client.addr[1]} ~ "
                          f"Preparing to broadcast message to "
                          f"<{client.username}>")
                    vp_send(conn=client.conn,
                            message=message,
                            private_key=self.private_key,
                            public_key=client.public_key,
                            receiver=client.username,
                            verbose=True)
                    print(f"\n[*] {client.addr[0]}:{client.addr[1]} ~ "
                          f"Successfully broadcast message from "
                          f"<{connection.username}> to: "
                          f"<{client.username}> {self.datestamp()}")
                except NetworkError:
                    self.remove_client(client)

    def remove_client(self, connection):
        for client in self.connections:
             if client.username == connection.username:
                self.connections.remove(client)
        connection.conn.close()
        print(f"\n[!] User <{connection.username}> disconnected "
              f"{self.datestamp()}")

    @staticmethod
    def datestamp():
        return f"@ {datetime.now().strftime('%m/%d/%Y-%H:%M:%S')}"
