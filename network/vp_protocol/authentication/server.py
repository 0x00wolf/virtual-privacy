import socket
from datetime import datetime

from Crypto.PublicKey import RSA

import crypter
from network.NetworkError import NetworkError
from network.vp_protocol.vp_recv import vp_recv
from network.vp_protocol.vp_send import vp_send
from runtime.database.key_exists import key_exists
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
        public_key = crypter.chacha20_poly1305.decrypt(
            unwrapped_key=unwrapped_key,
            ciphertext=ciphertext)
        if verbose:
            print(f"[ ] Successfully decrypted message. Checking if contents"
                  f"are a match for a stored key in the local SQL database.")
        exists = key_exists(
            database_path=database_path,
            public_key=public_key)
        if exists:
            imported_key = crypter.rsa.key.load_key(
                pem_string=public_key)
        else:
            raise NetworkError(message=f"")
        if verbose:
            print(f"[ ] Good public key. Key matches stored key in SQL "
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


def decoy(connection: socket.socket):
    response_body = ('<center><iframe width="560" height="315" '
                     'src="https://www.youtube.com/embed/dQw4w9WgXcQ?si=t-l'
                     'ER69FkSgEK4Dx&amp;controls=0" title="YouTube video '
                     'player" frameborder="0" allow="accelerometer; autoplay; '
                     'clipboard-write; encrypted-media; gyroscope; picture-in-'
                     'picture; web-share" allowfullscreen></iframe></center>')
    response_status = "HTTP/1.1 200 OK"
    response_headers = f"Content-Length: {len(response_body)}\r\n\r\n"
    response = f"{response_status}\r\n{response_headers}{response_body}"