import sqlite3
from runtime.database.DatabaseError import DatabaseError


def delete_key(key_id: int, database_path: str):
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        confirm = input(f"[*] Confirm operation: Delete target key "
                        f"(id: {key_id})\n"
                        f"[>] (y/n): ")
        cursor.execute('''DELETE FROM public_keys WHERE id = ?
        ''', (key_id,))
        conn.commit()
        conn.close()
        print(f"[*] Key deleted")
    except (ValueError, TypeError) as e:
        raise DatabaseError(message=f"{e}")
