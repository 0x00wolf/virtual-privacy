import socket
from datetime import datetime

from Crypto.PublicKey import RSA

import crypter
from network.NetworkError import NetworkError
from network.vp_protocol.vp_recv import vp_recv
from network.vp_protocol.vp_send import vp_send
from runtime.database.functions import key_exists
from runtime.database.DatabaseError import DatabaseError


def chat_server(database_path: str,
                private_key: RSA.RsaKey,
                conn: socket.socket,
                addr: tuple,
                connections: list,
                banner: str,
                verbose: bool = False) -> (str, RSA.RsaKey | None, None):
    try:
        payload = conn.recv(400)
        if verbose:
            print(f"[*] {addr[0]}:{addr[1]} ~ Received 400 bytes buffer ("
                  f"wrapped key & protocol header) @ "
                  f"{datetime.now().strftime('%m/%d/%Y-%H:%M:%S')}")
            print(f"[ ] First 8 bytes of buffer: {payload[:8]}")
        vp_protocol_header = payload[384:]
        message_length = int(vp_protocol_header, 2)
        if verbose:
            print(f"[ ] VP protocol header: "
                  f"{vp_protocol_header.decode()}")
    except (OSError, ValueError) as e:
        raise NetworkError(message=f"{e}")
    # Attempt to unwrap the 256-bit session key
    if verbose:
        print(f"[ ] Attempting to unwrap buffer using server's {private_key} ")
    try:
        unwrapped_key = crypter.rsa.unwrap(
            private_key=private_key,
            wrapped_key=payload[:384])
        if verbose:
            print(f"[ ] Session key successfully unwrapped."
                  f"\n[ ] First 8 bytes of session key: {unwrapped_key[:8]}")
        # Attempt to receive the sender's signature and ciphertext username
        try:
            buffer = conn.recv(message_length)
            signature = buffer[:384]
            ciphertext = buffer[384:]
            if verbose:
                print(f"[*] Received {message_length} payload (signature & "
                      f"ciphertext) "
                      f" {datetime.now().strftime('%m/%d/%Y-%H:%M:%S')}")
        except OSError as e:
            raise NetworkError(message=f"{e}")
        public_key = crypter.chacha20_poly1305.decrypt(
            unwrapped_key=unwrapped_key,
            ciphertext=ciphertext)
        if verbose:
            print(f"[ ] Message decrypted successful."
                  f"\n[ ] Verifying message contents are a known RSA public "
                  f"key.")
        exists = key_exists(
            database_path=database_path,
            public_key=public_key)
        if exists:
            imported_key = crypter.rsa.key.load_key(
                pem_string=public_key)
        else:
            raise NetworkError(message=f"")
        if verbose:
            print(f"[ ] Good key! Key found in SQL "
                  f"database.")
        good_signature = crypter.rsa.verify(
            public_key=imported_key,
            signature=signature,
            bytes_string=public_key.encode())
        if good_signature:
            if verbose:
                print(f"[*] {addr[0]}:{addr[1]} ~ Authentication "
                      f"Successful - signature verified! "
                      f"\n[ ] Importing client's RSA public key.")
        public_key = crypter.rsa.key.load_key(pem_string=public_key)
        try:
            print(f"\n[*] {addr[0]}:{addr[1]} ~ Sending username prompt @ "
                  f"{datetime.now().strftime('%m/%d/%Y-%H:%M:%S')}")
            vp_send(
                conn=conn,
                message='Username: ',
                private_key=private_key,
                public_key=public_key,
                verbose=True,
                receiver='receiver')
        except OSError as e:
            raise NetworkError(
                message=f"{addr[0]}:{addr[1]} ~ Connection error {e} @ "
                        f"{datetime.now().strftime('%m/%d/%Y-%H:%M:%S')}")
        try:
            username = vp_recv(
                conn=conn,
                private_key=private_key,
                public_key=imported_key,
                verbose=True)
            if verbose:
                print(f"[*] {addr[0]}:{addr[1]} ~ Username set: <{username}> "
                      f" @ {datetime.now().strftime('%m/%d/%Y-%H:%M:%S')}")
        except OSError as e:
            raise NetworkError(
                message=f"{addr[0]}:{addr[1]} ~ Connection error {e} @ "
                        f"{datetime.now().strftime('%m/%d/%Y-%H:%M:%S')}")
        if verbose:
            print(f"\n[*] {addr[0]}:{addr[1]} ~ Sending <{username}> "
                  f"banner message.")
        vp_send(conn=conn,
                message=banner,
                private_key=private_key,
                public_key=public_key,
                receiver=username,
                verbose=True)
        return username, public_key
    except (crypter.CrypterError, DatabaseError) as e:
        raise NetworkError(message=f"{e}")
