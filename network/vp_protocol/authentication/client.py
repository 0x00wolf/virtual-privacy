import socket
from datetime import datetime

from Crypto.PublicKey import RSA

import crypter
from network.NetworkError import NetworkError
from network.vp_protocol.vp_send import vp_send
from network.vp_protocol.vp_recv import vp_recv


def client(public_key: RSA.RsaKey,
           private_key: RSA.RsaKey,
           conn: socket.socket) -> None:
    try:
        validation_key = crypter.rsa.key.ret_public_pem_from(private_key)
        wrapped_key, signature, ciphertext = \
            crypter.encrypt.signed_message(encoded_string=validation_key,
                                           public_key=public_key,
                                           private_key=private_key,
                                           verbose=True)
    except crypter.CrypterError as e:
        raise NetworkError(message=f"{e}")
    try:
        conn.sendall(wrapped_key)
        print(f"[*] Sent to server: Wrapped session key, 384 bytes @ "
              f"{datetime.now().strftime('%m/%d/%Y-%H:%M:%S')}")
    except OSError as e:
        raise NetworkError(message=f"{e}")
    try:
        conn.sendall(signature)
        print(f"[*] Sent to server: Signature, 384 bytes "
              f"{datetime.now().strftime('%m/%d/%Y-%H:%M:%S')}")
        message_length = len(ciphertext)
        binary = bin(message_length)[2:]
        vp_protocol_header = binary.rjust(12, '0')
        conn.sendall(vp_protocol_header.encode())
        print(f"[*] Sent to server: Fixed length protocol header <"
              f"{vp_protocol_header}> 12 bytes @ "
              f"{datetime.now().strftime('%m/%d/%Y-%H:%M:%S')}")
        conn.sendall(ciphertext.encode())
        conn.sendall(b'\n')
        print(f"[ ] Authentication submitted successfully @ "
              f"{datetime.now().strftime('%m/%d/%Y-%H:%M:%S')}")
    except (OSError, TypeError) as e:
        raise NetworkError(message=f"{e}")
