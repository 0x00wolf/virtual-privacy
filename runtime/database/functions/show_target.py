import sqlite3
from runtime.database.DatabaseError import DatabaseError


def show_target(server_nickname: str, database_path: str):
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT Host, port, public_key, certificate
            FROM targets
            WHERE target_name = ?
        ''', (server_nickname,))
        result = cursor.fetchone()
        conn.close()
        print(f"[*] Target nickname: {server_nickname}"
              f"\n[ ] Host: {result[0]}"
              f"\n[ ] port: {result[1]}"
              f"\n[ ] public_key:\n{result[2]}"
              f"\n[ ] certificate: {result[3]}")
    except (TypeError, ValueError) as e:
        raise DatabaseError(message=f"{e}")
