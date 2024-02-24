import json
import socket
from datetime import datetime

from Crypto.PublicKey import RSA

import crypter
from runtime.database.functions import key_exists
from network.NetworkError import NetworkError
from runtime.database.DatabaseError import DatabaseError


def server(database_path: str,
           private_key: RSA.RsaKey,
           conn: socket.socket,
           addr: tuple,
           verbose: bool = False) -> (str, RSA.RsaKey | None, None):
    try:
        wrapped_key = conn.recv(384)
        print(f"[*] {addr[0]}:{addr[1]} ~ Received 384 bytes buffer "
              f"{datetime.now().strftime('%m/%d/%Y-%H:%M:%S')}")
        print(f"[ ] First 8 bytes of buffer: {wrapped_key[:8]}")
    except OSError as e:
        decoy(connection=conn)
        raise NetworkError(message=f"{e}")
    # Attempt to unwrap the 256-bit session key
    if verbose:
        print(f"[ ] Attempting to unwrap buffer using server's {private_key} ")
    try:
        unwrapped_key = crypter.rsa.unwrap(
            private_key=private_key,
            wrapped_key=wrapped_key)
        if verbose:
            print(f"[ ] Session key successfully unwrapped. First 10 bytes: "
                  f"{unwrapped_key[:10]}")
        # Attempt to receive the sender's signature and ciphertext username
        try:
            payload = conn.recv(400)
            if verbose:
                print(f"\n[*] {addr[0]}:{addr[1]} "
                      f"~ Received 400 byte payload @ "
                      f"{datetime.now().strftime('%m/%d/%Y-%H:%M:%S')}")
            signature = payload[:384]
            vp_protocol_header = payload[384:].decode()
            if verbose:
                print(f"[ ] VP fixed length protocol header: "
                      f"{vp_protocol_header}")
            message_length = int(vp_protocol_header, 2)
            ciphertext = conn.recv(message_length)
            cipher_t = json.loads(ciphertext)
            if verbose:
                print(f"[ ] Ciphertext length in bytes: {len(ciphertext)}"
                      f"\n[ ] Ciphertext (first 32 bytes): "
                      f"{cipher_t['ciphertext'][:32]}")
        except OSError as e:
            raise NetworkError(message=f"{e}")
        public_key = crypter.chacha20_poly1305.decrypt(
            unwrapped_key=unwrapped_key,
            ciphertext=ciphertext)
        if verbose:
            print(f"[ ] Successfully decrypted message. Checking if contents"
                  f"are a match for a stored RSA public key.")
        exists = key_exists(
            database_path=database_path,
            public_key=public_key)
        if exists:
            imported_key = crypter.rsa.key.load_key(
                pem_string=public_key)
        else:
            raise NetworkError(message=f"")
        if verbose:
            print(f"[ ] Good public key. Key found in runtime in SQL "
                  f"database.")
        good_signature = crypter.rsa.verify(
            public_key=imported_key,
            signature=signature,
            bytes_string=public_key.encode())
        if good_signature:
            if verbose:
                print(f"[*] {addr[0]}:{addr[1]} ~ Authentication "
                      f"Successful - good RSA signature for key!")
        public_key = crypter.rsa.key.load_key(pem_string=public_key)
        print(f"[*] {addr[0]}:{addr[1]} ~ Successfully authenticated at "
              f"{datetime.now().strftime('%m/%d/%Y-%H:%M:%S')}")
        return public_key
    except (crypter.CrypterError, DatabaseError) as e:
        raise NetworkError(message=f"{e}")
