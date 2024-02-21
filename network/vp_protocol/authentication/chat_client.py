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
        message_length = len(ciphertext) + 384
        binary = bin(message_length)[2:]
        vp_protocol_header = binary.rjust(16, '0')
        print(f"[ ] VP fixed length message header: {vp_protocol_header}")
        conn.sendall(wrapped_key + vp_protocol_header.encode())
        print(f"[*] Sent 400 byte buffer (wrapped key & protocol header) "
              f"{datetime.now().strftime('%m/%d/%Y-%H:%M:%S')}")
    except (OSError, TypeErro) as e:
        raise NetworkError(message=f"{e}")
    try:
        print(f"[*] Sending {len(ciphertext) + 383} byte payload (ciphertext "
              f"signature) @ {datetime.now().strftime('%m/%d/%Y-%H:%M:%S')}")
        conn.sendall(signature + ciphertext.encode())
        print(f"[ ] Authentication submitted successfully @ "
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
