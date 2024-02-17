import sqlite3
from runtime.database.DatabaseError import DatabaseError


def delete_target(server_nickname: str, database_path: str):
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        confirm = input(f"[*] Confirm operation: Delete target server "
                        f"<{server_nickname}>?"
                        f"\n[>] (y/n): ")
        cursor.execute('''DELETE FROM targets WHERE target_name = ?
        ''', (server_nickname,))
        conn.commit()
        conn.close()
    except (ValueError, TypeError) as e:
        raise DatabaseError(message=f"{e}")
