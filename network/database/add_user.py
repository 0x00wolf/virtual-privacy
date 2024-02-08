import sqlite3
from network.database.DatabaseError import DatabaseError


def add_user(database_path, username, rsa_public_key):
    try:
        con = sqlite3.connect(database_path)
        cursor = con.cursor()
        # Check if the username already exists
        cursor.execute("SELECT username FROM users WHERE username = ?",
                       (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            raise ValueError("Username already exists")
        with open(rsa_public_key, 'r') as f:
            public_key = f.read()
        cursor.execute("INSERT INTO users "
                       "(username, rsa_public_key) "
                       "VALUES (?, ?)", (username, public_key))
        con.commit()
        con.close()
        print(f"[*] User <{username}> added to SQL database.")
    except (ValueError, TypeError) as e:
        raise DatabaseError(message=f"{e}")

