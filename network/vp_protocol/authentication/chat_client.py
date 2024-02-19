import socket
from datetime import datetime

from Crypto.PublicKey import RSA

import crypter.encrypt
import crypter.CrypterError
from network.NetworkError import NetworkError
from network.vp_protocol.vp_send import vp_send
from network.vp_protocol.vp_recv import vp_recv
from crypter.rsa.key.ret_public_pem_from import ret_public_pem_from


def chat_client(public_key: RSA.RsaKey,
                private_key: RSA.RsaKey,
                conn: socket.socket) -> None:
    try:
        validation_key = ret_public_pem_from(private_key)
        wrapped_key, signature, ciphertext = \
            crypter.encrypt.signed_message(encoded_string=validation_key,
                                           public_key=public_key,
                                           private_key=private_key,
                                           verbose=True)
    except crypter.CrypterError as e:
        raise NetworkError(message=f"{e}")
    try:
        conn.sendall(wrapped_key)
        print(f"[*] Sent wrapped session key, 384 bytes "
              f"{datetime.now().strftime('%m/%d/%Y-%H:%M:%S')}")
    except OSError as e:
        raise NetworkError(message=f"{e}")
    try:
        print(f"[*] Sent to server: Signature, 384 bytes "
              f"{datetime.now().strftime('%m/%d/%Y-%H:%M:%S')}")
        message_length = len(ciphertext)
        binary = bin(message_length)[2:]
        vp_protocol_header = binary.rjust(12, '0')
        buffer = (signature + vp_protocol_header.encode())
        conn.sendall(buffer)
        print(f"[*] Sent 396 byte buffer to server. buffer[:384]='signature', "
              f"buffer[384:]='protocol header' @"
              f"{datetime.now().strftime('%m/%d/%Y-%H:%M:%S')}"
              f"\n[ ] VP fixed length protocol header: {vp_protocol_header}")
        conn.sendall(ciphertext.encode())
        conn.sendall(b'\n')
        print(f"[ ] Authentication submitted successfully "
              f"{datetime.now().strftime('%m/%d/%Y-%H:%M:%S')}")
        prompt = vp_recv(
            conn=conn,
            private_key=private_key,
            public_key=public_key,
            verbose=True)
        if not prompt:
            raise NetworkError(message="Connection error, server is not "
                                       "responding.")
        username = input(prompt)
        vp_send(
            conn=conn,
            message=username,
            private_key=private_key,
            public_key=public_key,
            receiver='server',
            verbose=True)
        banner = vp_recv(conn=conn,
                         private_key=private_key,
                         public_key=public_key,
                         verbose=True)
        print(banner)
    except (OSError, TypeError) as e:
        raise NetworkError(message=f"{e}")
