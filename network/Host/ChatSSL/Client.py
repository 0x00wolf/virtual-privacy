import ssl
import socket
import base64
import readline
import threading
from datetime import datetime

import crypter
from network.NetworkError import NetworkError
from network.vp_protocol.b64_send import b64_send
from network.vp_protocol.b64_recv import b64_recv


class Client:
    def __init__(self, host, port, certificate):
        self.host = host
        self.port = port
        self.certificate = certificate

    def run(self):
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            context.load_verify_locations(self.certificate)
        except OSError as e:
            raise NetworkError(message=f"[!] SSL context creation error {e}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
            with context.wrap_socket(conn, server_side=False,
                                     server_hostname=self.host) as ssock:
                try:
                    ssock.connect((self.host, self.port))
                except (ssl.SSLCertVerificationError, ConnectionError) as e:
                    raise NetworkError(message=f"{e}")
                print(f"[ ] SSL protocol version: {ssock.version()}")
                prompt = b64_recv(conn=ssock)
                username = self.input_with_history(prompt)
                b64_send(message_str=username, conn=ssock)
                banner = b64_recv(conn=ssock)
                print(banner)
                try:
                    receiver = threading.Thread(
                        target=self.receive_messages, args=(ssock,),
                        daemon=True)
                    receiver.start()
                    while True:
                        message = input()
                        if not message:
                            pass
                        else:
                            try:
                                b64_send(message_str=message, conn=ssock)
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
