import sqlite3

from runtime.database.DatabaseError import DatabaseError


def delete_key(key_id: int, database_path: str, nickname:str = None):
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        if nickname:
            cursor.execute("SELECT id FROM public_keys WHERE nickname = ?",
                           (nickname,))
            matching_key = cursor.fetchone()
        else:
            cursor.execute("Select id FROM public_keys WHERE id = ?",
                            (nickname,))
            matching_key = cursor.fetchone()
        if not matching_key:
            raise ValueError('Target nickname not found in user database.')
        insert_me = f"\n[ ] Nickname: {nickname}" if nickname else ''
        confirm = input(f"[*] Confirm operation: Delete target key "
                        f"(id: {matching_key})\n"
                        f"{insert_me}"
                        f"[>] (y/n): ")
        if confirm == 'y':
            cursor.execute('''DELETE FROM public_keys WHERE id = ?
                   ''', (key_id,))
        conn.commit()
        conn.close()
        print(f"[*] Key deleted")
    except (ValueError, TypeError) as e:
        raise DatabaseError(message=f"{e}")
