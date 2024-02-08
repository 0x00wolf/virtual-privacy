import socket
import threading
import queue
import sys

from network.Host import Host
from network.NetworkError import NetworkError


class Server(Host):
    def __init__(self, host, port, banner):
        super().__init__(host=host,
                         port=port,
                         banner=banner)

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            s.listen()
            print(f"listening on... {self.host}:{self.port}.")
            while True:
                conn, addr = s.accept()
                print(f"[*] {addr[0]}:{addr[1]} ~ connected "
                      f"{self.datestamp()}.")
                client = threading.Thread(
                    target=self.handle_client,
                    args=(conn, addr))
                client.start()

    def handle_client(self, conn, addr):
        with conn:
            conn.send(b'Username: ')
            username = conn.recv(self.buffer['SML']).decode()
            if not username:
                raise NetworkError(message=f"[!] {addr[0]}:{addr[1]} ~ Error "
                                           f"receiving username, dropping "
                                           f"connection {self.datestamp()}")
            else:
                print(f"[*] {addr[0]}:{addr[1]} ~ user: {username} connected "
                      f"{self.datestamp()}")
                conn.send(f"Welcome to {self.banner}".encode())
                self.connections.append(conn)
                self.broadcast(conn=conn, addr=addr, username=username)
                try:
                    while True:
                        data = conn.recv(self.buffer['MED']).decode()
                        if not data:
                            break
                        else:
                            print(f"[*] {addr[0]}:{addr[1]} ~ message "
                                  f"received {self.datestamp()}.")
                            self.broadcast(conn, addr, username, data)
                except OSError as e:
                    print(f"[!] {addr[0]}:{addr[1]} ~ disconnected "
                          f"{self.datestamp()}.")
                    self.remove_client(conn)

    def broadcast(self, conn, addr, username, data=None):
        for client in self.connections:
            if client != conn:
                try:
                    print(f"[>] broadcasting from {addr[0]}:{addr[1]} to "
                          f"{client.getpeername()[0]}:{client.getpeername()[1]} "
                          f"{self.datestamp()}.")
                    if not data:
                        client.send(f"{username} connected "
                                    f"{self.datestamp()}".encode())
                    else:
                        client.send(f"{username}: {data}".encode())
                except OSError as e:
                    print(f"[!] {addr[0]}:{addr[1]} ~ disconnected "
                          f"{self.datestamp()}.")
                    self.remove_client(conn)

    def remove_client(self, conn):
        if conn in self.connections:
            conn.close()
            self.connections.remove(conn)



