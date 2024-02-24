import socket
import base64

from network.NetworkError import NetworkError


def b64_recv(conn: socket.socket) -> str | None:
    try:
        vp_protocol_header = conn.recv(16).decode()
        message_length = int(vp_protocol_header, 2)
        message = base64.b64decode(conn.recv(message_length))
        end = conn.recv(1)
    except (OSError, ValueError, AttributeError) as e:
        raise NetworkError(message=f"receiving Base64 message {e}")
    return message.decode()
