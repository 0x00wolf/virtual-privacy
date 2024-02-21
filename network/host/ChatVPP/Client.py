import socket
import readline
import threading
from datetime import datetime

import crypter
from network.NetworkError import NetworkError
from network.vp_protocol.vp_recv import vp_recv
from network.vp_protocol.vp_send import vp_send
from crypter.encrypt.signed_message import signed_message
from network.vp_protocol.authentication.chat_client import (chat_client as
                                                            authentication)


class Client:
    def __init__(self, host, port, private_key, public_key):
        self.host = host
        self.port = port
        self.private_key = private_key
        self.public_key = public_key

    def run(self):
        with (socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn):
            try:
                conn.connect((self.host, self.port))
                print(f"\n[*] Connected to {self.host}:{self.port} @ "
                      f"{datetime.now().strftime('%m/%d/%Y-%H:%M:%S')}")
                print(f"[ ] Commencing authentication process...")
                authentication(
                    conn=conn,
                    public_key=self.public_key,
                    private_key=self.private_key)
            except (OSError, NetworkError, ConnectionError) as e:
                print(f"[!] Server rejected authentication: {e}")
                quit()
            try:
                receiver = threading.Thread(
                    target=self.receive_messages,
                    args=(conn, ),
                    daemon=True)
                receiver.start()
                while True:
                    message = input('')
                    if not message:
                        pass
                    else:
                        vp_send(conn=conn,
                                public_key=self.public_key,
                                private_key=self.private_key,
                                message=message)
            except (OSError, threading.ThreadError, NetworkError,
                    crypter.CrypterError, KeyboardInterrupt) as e:
                print(f"[!] Fatal error {e}")
                conn.close()

    def receive_messages(self, conn):
        while True:
            try:
                message = vp_recv(conn=conn,
                                  private_key=self.private_key,
                                  public_key=self.public_key)
                print(message)
            except NetworkError as e:
                print(f"[!] Fatal error: {e}")
                quit()

    @staticmethod
    def input_with_history(prompt):
        line = input(prompt)
        readline.add_history(line)
        return line
