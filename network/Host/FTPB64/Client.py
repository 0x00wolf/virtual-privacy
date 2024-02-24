import base64
import socket
import threading

from network.NetworkError import NetworkError


class Client:
    def __init__(self, host: str, port: int, file_out: str):
        self.host = host
        self.port = port
        self.file_out = file_out

    def run(self):
        with (socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s):
            try:
                s.settimeout(2)
                s.connect((self.host, self.port))
            except (ConnectionRefusedError, TimeoutError) as e:
                raise NetworkError(message=f"{e}")
            with open(self.file_out, 'wb') as f:
                i = 1
                while True:
                    try:
                        data = s.recv(1024)
                    except (TimeoutError, OSError) as e:
                        raise NetworkError(message=f"{e}")
                    if not data:
                        break
                    else:
                        print(f"receiving buffer{'.'*i}")
                        f.write(base64.b64decode(data))
                        if i == 3:
                            i = 1
                        else:
                            i += 1
            with open(self.file_out, 'r') as f:
                data = f.read()
            if data:
                print(f'[*] File successfully downloaded to: {self.file_out}')
            else:
                print(f"[!] Failed to download data, {self.file_out} empty.")
            s.close()
            print('[ ] Connection closed.\n[ ] Exiting...')
