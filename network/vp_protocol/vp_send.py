import socket

from Crypto.PublicKey import RSA

from crypter.encrypt.signed_message import signed_message
from crypter.CrypterError import CrypterError
from network.NetworkError import NetworkError


def vp_send(conn: socket.socket,
            message: str,
            private_key: RSA.RsaKey,
            public_key: RSA.RsaKey,
            receiver: str = None,
            verbose: bool = False) -> None:
    try:
        wrapped_key, signature, ciphertext = signed_message(
            encoded_string=message.encode(), public_key=public_key,
            private_key=private_key, receiver=receiver, verbose=verbose)
        buffer = wrapped_key + signature + ciphertext.encode()
        message_length = len(buffer)
        binary = bin(message_length)[2:]
        vp_protocol_header = binary.rjust(16, '0')
        conn.sendall(vp_protocol_header.encode())
        if verbose:
            print(f"[*] {conn.getpeername()[0]}:{conn.getpeername()[1]} ~ "
                  f"Sent 16 byte fixed length protocol header")
        conn.sendall(buffer)
        if verbose:
            print(f"[*] {conn.getpeername()[0]}:{conn.getpeername()[1]} ~ "
                  f"Sent {message_length} byte payload")
    except (OSError, ValueError, CrypterError) as e:
        raise NetworkError(message=f"VP-Protocol send error {e}")