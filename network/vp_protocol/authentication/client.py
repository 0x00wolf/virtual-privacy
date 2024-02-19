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
        print(f"[*] Sent RSA wrapped 256-bit session key to server (384 bytes) "
              f"@ {datetime.now().strftime('%m/%d/%Y-%H:%M:%S')}")
    except OSError as e:
        raise NetworkError(message=f"{e}")
    try:
        message_length = len(ciphertext)
        binary = bin(message_length)[2:]
        vp_protocol_header = binary.rjust(12, '0')
        payload = signature + vp_protocol_header.encode()
        conn.sendall(payload)
        print(f"[*] Transmitted 396 byte payload (signature and VP header) @"
              f"{datetime.now().strftime('%m/%d/%Y-%H:%M:%S')}"
              f"\n[ ] VP fixed length protocol header: "
              f"{vp_protocol_header}")
        conn.sendall(ciphertext.encode())
        print(f"[ ] Authentication submitted successfully @ "
              f"{datetime.now().strftime('%m/%d/%Y-%H:%M:%S')}")
    except (OSError, TypeError) as e:
        raise NetworkError(message=f"{e}")
