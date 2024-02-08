import sys
import socket
import threading
import crypter
import network.vp_protocol.receive_v2

from network.Host import Host
from network.NetworkError import NetworkError
from crypter.encrypt.signed_message import signed_message
from network.vp_protocol.send_v2 import send_v2 as vp_protocol_send
from network.vp_protocol.receive_v2 import receive_v2 as vp_protocol_receive


class Client(Host):
    def __init__(self, host, port, private_key, public_key):
        super().__init__(host=host,
                         port=port,
                         private_key=private_key,
                         public_key=public_key)

    def run(self):
        with (socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn):
            try:
                conn.connect((self.host, self.port))
                username = self.input_with_history('[*] Username: ')
                network.vp_protocol.authentication.client_side(
                    username=username,
                    conn=conn,
                    public_key=self.public_key,
                    private_key=self.private_key)
                banner = vp_protocol_receive(conn=conn,
                                             private_key=self.private_key,
                                             public_key=self.public_key,
                                             addr=None)
                if banner:
                    print(banner)
            except (OSError, NetworkError) as e:
                print(f"[!] Server rejected authentication: {e}")
                sys.exit()
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
                        vp_protocol_send(
                            conn=conn,
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
                message = vp_protocol_receive(
                    conn=conn,
                    private_key=self.private_key,
                    public_key=self.public_key,
                    addr=(f"{self.host}:", self.port))
                print(message)
            except NetworkError as e:
                print(f"[!] Fatal error: {e}")
                sys.exit()
