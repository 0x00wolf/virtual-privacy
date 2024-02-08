import sqlite3
from network.database.DatabaseError import DatabaseError


def show_user(database_path, username):
    try:
        con = sqlite3.connect(database_path)
        cur = con.cursor()
        query = ("SELECT username, rsa_public_key "
                 "FROM users WHERE username = ?")
        cur.execute(query, (username,))
        result = cur.fetchone()
        con.close()
        print(f"[*] Username: {result[0]}\n[*] RSA Public Key:\n{result[1]}")
    except (TypeError, ValueError) as e:
        raise DatabaseError(message=f"{e}")
