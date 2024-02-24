import base64
import socket
import readline
import threading

import crypter
from network.NetworkError import NetworkError
from network.vp_protocol.b64_send import b64_send
from network.vp_protocol.b64_recv import b64_recv


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
            try:
                conn.connect((self.host, self.port))
            except ConnectionRefusedError as e:
                raise NetworkError(message=f"{e}")
            prompt = b64_recv(conn=conn)
            username = self.input_with_history(prompt)
            b64_send(message_str=username, conn=conn)
            banner = b64_recv(conn=conn)
            print(banner)
            try:
                receiver = threading.Thread(target=self.receive_messages,
                                            args=(conn,),
                                            daemon=True)
                receiver.start()

                while True:
                    message = input()
                    if not message:
                        pass
                    else:
                        try:
                            b64_send(message_str=message, conn=conn)
                        except OSError as e:
                            print(f"[!] Connection error: {e}")
            except (KeyboardInterrupt, threading.ThreadError) as e:
                print(f"[!] Connection interrupted.\n[ ]Exiting... ")
                quit()

    @staticmethod
    def receive_messages(conn):
        while True:
            try:
                message = b64_recv(conn)
                if not message:
                    break
                else:
                    print(message)
            except (NetworkError, KeyboardInterrupt) as e:
                print(f"[!] Connection error {e}")
                quit()

    @staticmethod
    def input_with_history(prompt):
        line = input(prompt)
        readline.add_history(line)
        return line
