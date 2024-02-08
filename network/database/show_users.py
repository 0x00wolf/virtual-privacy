import sqlite3
from network.database.DatabaseError import DatabaseError


def show_users(database_path):
    try:
        con = sqlite3.connect(database_path)
        cur = con.cursor()
        for row in cur.execute("SELECT username FROM users"):
            print(row)
    except (TypeError, ValueError) as e:
        raise DatabaseError(message=e)
