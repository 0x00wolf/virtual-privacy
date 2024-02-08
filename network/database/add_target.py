import sqlite3
from Crypto.PublicKey import RSA
from network.database.DatabaseError import DatabaseError


def add_target(database_path: str,
               server_nickname: str,
               host: str,
               port: int,
               public_key: str,
               certificate: str = None):
    try:
        con = sqlite3.connect(database_path)
        cur = con.cursor()
        cur.execute("SELECT target_name FROM targets WHERE target_name= ? ",
                    (server_nickname,))
        existing_target = cur.fetchone()
        if existing_target:
            raise ValueError(f"Server <{server_nickname}> already exists in "
                             f"the SQL database.")
        with open(public_key, 'r') as f:
            rsa_public_key = f.read()
        cur.execute("INSERT INTO targets "
                    "(target_name, host, port, public_key, certificate) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (server_nickname, host, port, rsa_public_key, certificate))
        con.commit()
        con.close()
        print(f"[*] Server <{server_nickname}> added to SQL database.")
    except (ValueError, TypeError) as e:
        raise DatabaseError(message=f"{e}")
