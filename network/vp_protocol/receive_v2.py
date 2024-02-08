import socket

from Crypto.PublicKey import RSA

import crypter
from crypter.CrypterError import CrypterError
from network.NetworkError import NetworkError


def receive_v2(conn: socket.socket,
               private_key: RSA.RsaKey,
               public_key: RSA.RsaKey,
               addr: tuple = None,
               verbose: bool = False):
    try:
        wrapped_key = conn.recv(384)
        if verbose:
            print(f"[*] {addr[0]}:{addr[1]} ~ Received wrapped session key, "
                  f"384 bytes. First 10 bytes: {wrapped_key[:10]}")
        signature = conn.recv(384)
        if verbose:
            print(f"[*] {addr[0]}:{addr[1]} ~ Received signature, "
                  f"384 bytes. First 10 bytes: {signature[:10]}")
        vp_protocol_header = conn.recv(12)
        if verbose:
            print(f"[*] {addr[0]}:{addr[1]} ~ Received VP-Protocol fixed "
                  f"length binary header, 12 bytes. Header: "
                  f"{vp_protocol_header.decode()}")
        message_length = int(vp_protocol_header, 2)
        ciphertext = conn.recv(message_length)
        if verbose:
            print(f"[*] {addr[0]}:{addr[1]} ~ Received ciphertext:"
                  f" {ciphertext}")
        end = conn.recv(1)
    except (OSError, ValueError) as e:
        raise NetworkError(message=f"{e}")
    try:
        message = crypter.decrypt.signed_message(
            private_key=private_key,
            public_key=public_key,
            wrapped_key=wrapped_key,
            signature=signature,
            ciphertext=ciphertext.decode())
        return message
    except CrypterError as e:
        raise NetworkError(message=f"{e}")
