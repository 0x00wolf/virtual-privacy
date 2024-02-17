import socket
import base64

from network.NetworkError import NetworkError


def b64_send(message_str: str, conn: socket.socket) -> None:
    try:
        b64_message = base64.b64encode(message_str.encode())
        message_length = len(b64_message)
        binary = bin(message_length)[2:]
        vp_protocol_header = binary.rjust(16, '0')
        conn.sendall(vp_protocol_header.encode())
        conn.sendall(base64.b64encode(message_str.encode()))
        conn.sendall(b'\n')
    except (OSError, ValueError, AttributeError) as e:
        raise NetworkError(message=f"Send error {e}")
