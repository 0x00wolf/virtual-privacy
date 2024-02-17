import sqlite3
from runtime.database.DatabaseError import DatabaseError


def add_key(database_path, public_key):
    try:
        con = sqlite3.connect(database_path)
        cursor = con.cursor()
        with open(public_key, 'r') as f:
            new_key = f.read()
        # Check if the username already exists
        cursor.execute("SELECT public_key FROM public_keys "
                       "WHERE public_key = ?",
                       (new_key,))
        existing_key = cursor.fetchone()
        if existing_key:
            raise ValueError("RSA public key already stored in database.")
        cursor.execute("INSERT INTO public_keys "
                       "(public_key) VALUES (?)", (new_key,))
        con.commit()
        cursor.execute("SELECT last_insert_rowid()")
        new_id = cursor.fetchone()[0]

        con.close()
        print(f"[*] RSA public key added to SQL database.\n"
              f"[ ] ID: {new_id}")
    except (ValueError, TypeError, FileNotFoundError) as e:
        raise DatabaseError(message=f"{e}")
