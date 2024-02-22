import sqlite3
from runtime.database.DatabaseError import DatabaseError


def add_target(database_path: str,
               host: str,
               port: int,
               nickname: str,
               public_pem: str = None,
               certificate: str = None):
    try:
        con = sqlite3.connect(database_path)
        cursor = con.cursor()
        if public_pem:
            with open(public_pem, 'r') as f:
                new_key = f.read()
        if certificate:
            with open(certificate, 'r') as f:
                cert = f.read()
        cursor.execute("SELECT nickname FROM targets "
                       "WHERE nickname = ?",
                       (nickname,))
        existing_nickname = cursor.fetchone()
        if existing_nickname:
            raise ValueError("Error, server nickname found in database. "
                             "Please select another... ")
            # Insert the new key into the public_keys table
        cursor.execute(
            "INSERT INTO targets (nickname, host, port, public_key, "
            "certificate) "
            "VALUES (?, ?, ?, ? ?)",
            (nickname, host, port, new_key, cert))
        con.commit()
        cursor.execute("SELECT last_insert_rowid()")
        new_id = cursor.fetchone()[0]
        con.close()
        print(f"[*] SQL database entry successful:"
              f"\n[ ] Nickname: {nickname}"
              f"\n[ ] Host: {host}"
              f"\n[ ] Port: {port}")
        if public_pem:
            print(f"\n[ ] RSA public key: {public_pem}")
        if certificate:
            print(f"\n[ ] Certificate: {certificate}")
    except (ValueError, TypeError, FileNotFoundError) as e:
        raise DatabaseError(message=f"{e}")
