import sqlite3
from runtime.database.DatabaseError import DatabaseError


def add_key(database_path, public_key, nickname: str = None):
    try:
        con = sqlite3.connect(database_path)
        cursor = con.cursor()
        with open(public_key, 'r') as f:
            new_key = f.read()
        cursor.execute("SELECT public_key FROM public_keys "
                       "WHERE public_key = ?",
                       (new_key,))
        existing_key = cursor.fetchone()
        if existing_key:
            raise ValueError("RSA public key already stored in database.")
        if nickname:
            cursor.execute(
                "SELECT nickname FROM public_keys WHERE nickname = ?",
                (nickname,))
            existing_nickname = cursor.fetchone()
            if existing_nickname:
                raise ValueError("Nickname already exists in the database.")
            # Insert the new key into the public_keys table
        cursor.execute(
            "INSERT INTO public_keys (public_key, nickname) VALUES (?, ?)",
            (new_key, nickname))
        con.commit()
        cursor.execute("SELECT last_insert_rowid()")
        new_id = cursor.fetchone()[0]

        con.close()
        if nickname:
            print(f"[*] SQL database entry successful:"
                  f"\n[ ] ID: {new_id}"
                  f"\n[ ] Client nickname: {nickname}"
                  f"\n[ ] RSA public key: {new_key}")
        else:
            print(f"[*] SQL database entry successful:"
                  f"\n[ ] ID: {new_id}"
                  f"\n[ ] RSA public key: {new_key}")
    except (ValueError, TypeError, FileNotFoundError) as e:
        raise DatabaseError(message=f"{e}")
