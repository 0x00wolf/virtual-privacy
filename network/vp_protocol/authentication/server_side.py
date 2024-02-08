import socket
from datetime import datetime

from Crypto.PublicKey import RSA

import crypter
from network.NetworkError import NetworkError
from network.database.DatabaseError import DatabaseError
from network.database.get_public_key import get_public_key
from network.vp_protocol.send_v2 import send_v2 as vp_protocol_send


def server_side(database_path: str,
                private_key: RSA.RsaKey,
                conn: socket.socket,
                addr: tuple,
                connections: list,
                banner: str,
                verbose: bool = False) -> (str, RSA.RsaKey | None, None):
    try:
        wrapped_key = conn.recv(384)
        print(f"[*] {addr[0]}:{addr[1]} ~ Received 384 bytes buffer "
              f"{datetime.now().strftime('%m/%d/%Y-%H:%M:%S')}")
    except OSError as e:
        raise NetworkError(message=f"{e}")
    # Attempt to unwrap the 256-bit session key
    if verbose:
        print(f"[ ] Attempting to unwrap buffer using server's {private_key} ")
    try:
        unwrapped_key = crypter.rsa.unwrap(private_key=private_key,
                                           wrapped_key=wrapped_key)
        if verbose:
            print(f"[ ] Session key successfully unwrapped. First 10 bytes: "
                  f"{unwrapped_key[:10]}")
        # Attempt to receive the sender's signature and ciphertext username
        try:
            signature = conn.recv(384)
            if verbose:
                print(f"[*] Received 384 byte signature & VP-Protocol header"
                      f"{datetime.now().strftime('%m/%d/%Y-%H:%M:%S')}")
            vp_protocol_header = conn.recv(12)
            if verbose:
                print(f"[*] Received Fixed length Protocol header, "
                      f"{vp_protocol_header}, 12 bytes "
                      f"{datetime.now().strftime('%m/%d/%Y-%H:%M:%S')}")
            message_length = int(vp_protocol_header, 2)
            ciphertext = conn.recv(message_length)
            end = conn.recv(1)
            if verbose:
                print(f"[*] Received ciphertext, {message_length} bytes:"
                      f" {ciphertext}")
        except OSError as e:
            raise NetworkError(message=f"{e}")
        username = crypter.chacha20_poly1305.decrypt(
            unwrapped_key=unwrapped_key,
            ciphertext=ciphertext)
        if verbose:
            print(f"[ ] Successfully decrypted ciphertext username: "
                  f"<{username}>. Verifying {username} is valid key in "
                  f"server's SQL database")

        public_pem = get_public_key(
            database_path=database_path,
            username=username)
        public_key = crypter.rsa.key.load_key(pem_string=public_pem)
        if verbose:
            print(f"[ ] Good username: {username}. "
                  f"\n[ ] {username.title()}'s {public_key} imported "
                  f"from SQL database.")
        good_signature = crypter.rsa.verify(public_key=public_key,
                                            signature=signature,
                                            bytes_string=username.encode())
        if good_signature:
            if verbose:
                print(f"[*] {addr[0]}:{addr[1]} ~ Authentication "
                      f"Successful - good signature! "
                      f"{username} connected "
                      f"{datetime.now().strftime('%m/%d/%Y-%H:%M:%S')}")

            for client in connections:
                if client.username == username:
                    print(f"[!] {addr[0]}:{addr[1]} ~ Trying to connect as "
                          f"{username}, who is currently logged in. "
                          f"Disconnecting "
                          f"{datetime.now().strftime('%m/%d/%Y-%H:%M:%S')}")
                    raise NetworkError(
                        message=f"Error, trying to log in as {username}, "
                                f"who is already logged in.")
            try:
                vp_protocol_send(conn=conn,
                                 message=banner,
                                 private_key=private_key,
                                 public_key=public_key,
                                 verbose=True)
            except OSError as e:
                raise NetworkError(message=f"[!] {addr[0]}:{addr[1]} ~ "
                                           f"Connection error: {e}")
            return username, public_key
        else:
            return None, None
    except (crypter.CrypterError, DatabaseError) as e:
        raise NetworkError(message=f"{e}")
