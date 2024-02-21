import sqlite3

from runtime.database.DatabaseError import DatabaseError


def show_key(database_path, target):
    try:
        if not key_id and not nickname:
            raise ValueError('Operation requires an ID or target nickname.')
        con = sqlite3.connect(database_path)
        cur = con.cursor()
        try:
            query = ("SELECT id, nickname, public_key "
                     "FROM public_keys WHERE nickname = ?")
            cur.execute(query, (target,))
            result = cur.fetchone()
        except ValueError:
            pass
        if not result:
            query = ("SELECT id, nickname, public_key "
                     "FROM public_keys WHERE id = ?")
            cur.execute(query, (nickname,))
            result = cur.fetchone()
        print(f"[*] Information on stored target:")
        print(result)
        con.close()
    except sqlite3.SQLITE_ERROR as e:
        raise DatabaseError(message=f"{e}")
    try:
        return result[0]
    except (ValueError, TypeError):
        raise DatabaseError(message="User not found in database")
