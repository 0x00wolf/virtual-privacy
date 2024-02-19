import base64
import socket
import threading

from Crypto.PublicKey import RSA

from network.NetworkError import NetworkError
from network.vp_protocol.vp_send import vp_send
from network.vp_protocol.vp_recv import vp_recv
from network.vp_protocol.authentication.client import client as vp_client_auth


class Client:
    def __init__(self,
                 host: str,
                 port: int,
                 file_out: str,
                 public_key: RSA.RsaKey,
                 private_key: RSA.RsaKey):
        self.host = host
        self.port = port
        self.file_out = file_out
        self.public_key = public_key
        self.private_key = private_key

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
            try:
                conn.connect((self.host, self.port))
            except (ConnectionRefusedError, TimeoutError) as e:
                raise NetworkError(message=f"{e}")
            vp_client_auth(conn=conn,
                           public_key=self.public_key,
                           private_key=self.private_key)
            with open(self.file_out, 'w') as f:
                i = 1
                while True:
                    try:
                        data = vp_recv(conn=conn,
                                       private_key=self.private_key,
                                       public_key=self.public_key,
                                       verbose=True)
                    except NetworkError:
                        break
                    if not data:
                        break
                    else:
                        print(f"receiving buffer{'.'*i}")
                        f.write(data)
                        if i == 3:
                            i = 1
                        else:
                            i += 1
            print(f'[*] File successfully downloaded to: {self.file_out}')
            conn.close()
            print('[ ] Connection closed.\n[ ] Exiting...')
