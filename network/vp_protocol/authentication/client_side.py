import socket
from datetime import datetime

from Crypto.PublicKey import RSA

import crypter
from network.NetworkError import NetworkError


def client_side(username: str,
                public_key: RSA.RsaKey,
                private_key: RSA.RsaKey,
                conn: socket.socket) -> None:
    try:
        wrapped_key, signature, ciphertext_username = \
            crypter.encrypt.signed_message(bytes_string=username.encode(),
                                           public_key=public_key,
                                           private_key=private_key,
                                           verbose=True)
    except crypter.CrypterError as e:
        raise NetworkError(message=f"{e}")
    try:
        conn.sendall(wrapped_key)
        print(f"[*] Sent to server: Wrapped session key, 384 bytes "
              f"{datetime.now().strftime('%m/%d/%Y-%H:%M:%S')}")
    except OSError as e:
        raise NetworkError(message=f"{e}")
    try:
        conn.sendall(signature)
        print(f"[*] Sent to server: Signature, 384 bytes "
              f"{datetime.now().strftime('%m/%d/%Y-%H:%M:%S')}")
        message_length = len(ciphertext_username)
        binary = bin(message_length)[2:]
        vp_protocol_header = binary.rjust(12, '0')
        conn.sendall(vp_protocol_header.encode())
        print(f"[*] Sent to server: Fixed length protocol header <"
              f"{vp_protocol_header}> 12 bytes "
              f"{datetime.now().strftime('%m/%d/%Y-%H:%M:%S')}")
        conn.sendall(ciphertext_username.encode())
        conn.sendall(b'\n')
        print(f"[ ] Authentication submitted successfully "
              f"{datetime.now().strftime('%m/%d/%Y-%H:%M:%S')}")
    except (OSError, TypeError) as e:
        raise NetworkError(message=f"{e}")
