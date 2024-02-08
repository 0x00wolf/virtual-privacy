import socket

from Crypto.PublicKey import RSA

from crypter.encrypt.signed_message import signed_message
from crypter.CrypterError import CrypterError
from network.NetworkError import NetworkError


def send_v2(conn: socket.socket,
            message: str,
            private_key: RSA.RsaKey,
            public_key: RSA.RsaKey,
            receiver: str = None,
            verbose: bool = False) -> None:
    try:
        wrapped_key, signature, ciphertext = signed_message(
            bytes_string=message.encode(),
            private_key=private_key,
            public_key=public_key,
            verbose=verbose)
    except CrypterError as e:
        raise NetworkError(f"{e}")
    receiver = f", to <{receiver}>" if receiver else ''
    try:
        conn.sendall(wrapped_key)
        if verbose:
            print(f"[*] Wrapped session key sent, 384 bytes{receiver} ")
        conn.sendall(signature)
        if verbose:
            print(f"[*] Signature sent, 384 bytes{receiver}")
        message_length = len(ciphertext.encode())
        binary = bin(message_length)[2:]
        vp_protocol_header = binary.rjust(12, '0')
        conn.sendall(vp_protocol_header.encode())
        if verbose:
            print(f"[*] VP protocol header sent{receiver}: "
                  f"{vp_protocol_header}")
        conn.sendall(ciphertext.encode())
        if verbose:
            print(f"[*] Ciphertext sent{receiver}: {ciphertext}")
        conn.sendall(b'\n')
    except (OSError, TypeError) as e:
        raise NetworkError(message=f"VP-Protocol send error: {e}")
