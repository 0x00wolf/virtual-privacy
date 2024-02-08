import sqlite3

from network.NetworkError import NetworkError
from network.database.DatabaseError import DatabaseError


def get_public_key(database_path, username):
    try:
        con = sqlite3.connect(database_path)
        cur = con.cursor()
        query = ("SELECT rsa_public_key "
                 "FROM users WHERE username = ?")
        cur.execute(query, (username,))
        result = cur.fetchone()
        con.close()
    except sqlite3.SQLITE_ERROR as e:
        raise DatabaseError(message=f"{e}")
    try:
        return result[0]
    except (ValueError, TypeError):
        raise DatabaseError(message="User not found in database")
