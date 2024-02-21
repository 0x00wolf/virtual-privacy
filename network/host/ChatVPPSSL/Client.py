import ssl
import socket
import threading

from Crypto.PublicKey import RSA

import crypter
from network.NetworkError import NetworkError
from network.vp_protocol.vp_send import vp_send
from network.vp_protocol.vp_recv import vp_recv
from network.vp_protocol.authentication.chat_client import (chat_client as
                                                            authentication)


class Client:
    def __init__(self,
                 host: str,
                 port: int,
                 private_key: RSA.RsaKey,
                 public_key: RSA.RsaKey,
                 certificate: str):
        self.host = host
        self.port = port
        self.private_key = private_key
        self.public_key = public_key
        self.certificate = certificate

    def run(self):
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_verify_locations(self.certificate)
        print(f"[*] SSL context loaded")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0) as sock:
            with context.wrap_socket(sock, server_side=False,
                                     server_hostname=self.host) as ssock:
                try:
                    ssock.connect((self.host, self.port))
                except (ConnectionError, ssl.SSLError) as e:
                    raise NetworkError(message=f"{e}")
                print(f"\n[*] Connected to {self.host}:{self.port}")
                print(f"[ ] SSL protocol version: {ssock.version()}")
                authentication(conn=ssock,
                               public_key=self.public_key,
                               private_key=self.private_key)
                try:
                    receiver = threading.Thread(target=self.receive_messages,
                                                args=(ssock,),
                                                daemon=True)
                    receiver.start()
                    while True:
                        message = input('')
                        if not message:
                            pass
                        else:
                            vp_send(conn=ssock,
                                    public_key=self.public_key,
                                    private_key=self.private_key,
                                    message=message)
                except (OSError, threading.ThreadError, NetworkError,
                        crypter.CrypterError, KeyboardInterrupt) as e:
                    print(f"[!] Fatal error {e}")
                    ssock.close()

    def receive_messages(self, ssock):
        while True:
            try:
                message = vp_recv(conn=ssock,
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
