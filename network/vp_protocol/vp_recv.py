import socket

from Crypto.PublicKey import RSA

import crypter
from crypter.CrypterError import CrypterError
from network.NetworkError import NetworkError


def vp_recv(conn: socket.socket,
            private_key: RSA.RsaKey,
            public_key: RSA.RsaKey,
            verbose: bool = False):
    try:
        vp_protocol_header = conn.recv(16).decode()
        if verbose:
            print(f"\n[*] {conn.getpeername()[0]}:{conn.getpeername()[1]} ~ "
                  f"Received 16 byte fixed length header: {vp_protocol_header}")
        message_length = int(vp_protocol_header, 2)
        buffer = conn.recv(message_length)
        if verbose:
            print(f"[*] {conn.getpeername()[0]}:{conn.getpeername()[1]} ~ "
                  f"Received {message_length} byte payload")
        wrapped_key = buffer[:384]
        signature = buffer[384:768]
        ciphertext = buffer[768:]
        message = crypter.decrypt.signed_message(
            private_key=private_key,
            public_key=public_key,
            wrapped_key=wrapped_key,
            signature=signature,
            ciphertext=ciphertext.decode(),
            verbose=verbose)
        return message
    except (CrypterError, OSError, ValueError) as e:
        raise NetworkError(message=f"{e}")
