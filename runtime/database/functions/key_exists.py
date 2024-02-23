import sqlite3

from runtime.database.DatabaseError import DatabaseError


def key_exists(database_path, public_key):
    try:
        con = sqlite3.connect(database_path)
        cur = con.cursor()
        query = ("SELECT public_key "
                 "FROM public_keys WHERE public_key = ?")
        cur.execute(query, (public_key,))
        result = cur.fetchone()
        con.close()
        if result:
            return True
        else:
            return False
    except sqlite3.SQLITE_ERROR as e:
        raise DatabaseError(message=f"{e}")
    except (ValueError, TypeError):
        raise DatabaseError(message="RSA public key not found in database")
