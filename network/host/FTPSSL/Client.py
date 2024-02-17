import ssl
import socket
import base64
import threading

from network.NetworkError import NetworkError


class Client:
    def __init__(self, host: str, port: int, file_out: str, certificate: str):
        self.host = host
        self.port = port
        self.file_out = file_out
        self.certificate = certificate

    def run(self):
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            context.load_verify_locations(cafile=self.certificate)
        except OSError as e:
            raise NetworkError(message=f"[!] SSL context creation error {e}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            with context.wrap_socket(sock, server_side=False,
                                     server_hostname=self.host) as ssock:
                try:
                    ssock.connect((self.host, self.port))
                except (ConnectionRefusedError, ssl.SSLError) as e:
                    raise NetworkError(message=f"{e}")
                print(f"[ ] SSL protocol version: {ssock.version()}")
                with open(self.file_out, 'wb') as f:
                    i = 1
                    while True:
                        data = ssock.recv(1024)
                        if not data:
                            break
                        else:
                            print(f"receiving buffer{'.' * i}")
                            f.write(base64.b64decode(data))
                            if i == 3:
                                i = 1
                            else:
                                i += 1
                print(f'[*] File successfully downloaded to: {self.file_out}'
                      f'\n[ ] Connection closed.'
                      f'\n[ ] Exiting...')
