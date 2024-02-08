import socket
import threading
import queue
import sys

from Crypto.PublicKey import RSA

import crypter
from network.Host import Host
from network.Connection import Connection
from network.NetworkError import NetworkError
from network.database.get_public_key import get_public_key
from network.vp_protocol.send_v2 import send_v2 as vp_protocol_send
from network.vp_protocol.receive_v2 import receive_v2 as vp_protocol_recv
from network.vp_protocol.authentication.server_side import server_side as \
    server_side_authentication


class Server(Host):
    def __init__(self,
                 host,
                 port,
                 banner,
                 private_key: RSA.RsaKey,
                 database_path):
        super().__init__(host=host,
                         port=port,
                         banner=banner,
                         private_key=private_key,
                         database_path=database_path)

    def run(self):
        with (socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s):
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            s.listen()
            print(f"[*] Secure chat server listening on: {self.host}"
                  f":{self.port}.")
            while True:
                try:
                    conn, addr = s.accept()
                except OSError:
                    print(f"[!] {addr[0]}:{addr[1]} ~ Connection error, "
                          f"disconnecting {self.datestamp()}")
                    continue
                try:
                    username, public_key = server_side_authentication(
                        private_key=self.private_key,
                        database_path=self.database_path,
                        conn=conn,
                        addr=addr,
                        connections=self.connections,
                        banner=self.banner,
                        verbose=True)
                except NetworkError as e:
                    print(f"[!] {addr[0]}:{addr[1]} ~ Authentication failed: "
                          f"{e}")
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
                    message = vp_protocol_recv(
                        conn=connection.conn,
                        addr=connection.addr,
                        public_key=connection.public_key,
                        private_key=self.private_key,
                        verbose=True)
                    if not message:
                        raise NetworkError
                    else:
                        print(f"[*] {connection.addr[0]}:"
                              f"{connection.addr[1]} ~ "
                              f"<{connection.username.title()}>'s decrypted "
                              f"message: {message} ")
                        self.broadcast(connection=connection,
                                       data=message)
                except (NetworkError, crypter.CrypterError) as e:
                    print(f"[*] {connection.addr[0]}:{connection.addr[1]} ~ "
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
                    print(f"[*] {client.addr[0]}:{client.addr[1]} ~ "
                          f"Preparing to broadcast message to "
                          f"<{client.username}>")
                    vp_protocol_send(conn=client.conn,
                                     message=message,
                                     private_key=self.private_key,
                                     public_key=client.public_key,
                                     receiver=client.username,
                                     verbose=True)
                    print(f"[*] {client.addr[0]}:{client.addr[1]} ~ "
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
        print(f"[!] User <{connection.username}> disconnected "
              f"{self.datestamp()}")
