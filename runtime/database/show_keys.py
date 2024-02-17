import sqlite3


def show_keys(database_path):
    try:
        con = sqlite3.connect(database_path)
        cur = con.cursor()
        [print(row) for row in cur.execute("SELECT id, public_key "
                                           "FROM public_keys")]
    except (TypeError, ValueError) as e:
        raise DatabaseError(message=e)
