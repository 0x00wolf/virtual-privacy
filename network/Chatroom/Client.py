import sys
import socket
import threading
import crypter

from network.Host import Host


class Client(Host):
    def __init__(self, host, port):
        super().__init__(host=host,
                         port=port)

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
            conn.connect((self.host, self.port))
            prompt = conn.recv(self.buffer['SML']).decode()
            username = self.input_with_history(prompt)
            conn.sendall(username.encode())
            banner = conn.recv(self.buffer['SML']).decode()
            print(banner)
            receiver = threading.Thread(target=self.receive_messages,
                                        args=(conn,))
            receiver.start()
            while True:
                message = input()
                if not message:
                    pass
                else:
                    try:
                        conn.sendall(message.encode())
                    except OSError as e:
                        print(f"[!] Connection error: {e}")

    def receive_messages(self, conn):
        while True:
            message = conn.recv(self.buffer['MED'])
            if not message:
                break
            else:
                print(f"{message.decode('utf-8')}")
