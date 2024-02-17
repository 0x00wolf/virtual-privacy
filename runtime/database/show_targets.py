import sqlite3
from runtime.database.DatabaseError import DatabaseError


def show_targets(database_path):
    try:
        con = sqlite3.connect(database_path)
        cur = con.cursor()
        [print(row) for row in cur.execute("SELECT target_name FROM targets")]
    except (TypeError, ValueError) as e:
        raise DatabaseError(message=e)
