import sqlite3
from runtime.database.DatabaseError import DatabaseError


def create_database(database_path):
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        # Create the users table if it doesn't exist
        cursor.execute("CREATE TABLE IF NOT EXISTS public_keys "
                       "(id INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "nickname TEXT, "
                       "public_key TEXT)")
        # Create the targets table if it doesn't exist
        cursor.execute("CREATE TABLE IF NOT EXISTS targets "
                       "(target_name TEXT PRIMARY KEY, "
                       "Host TEXT, "
                       "port INTEGER, "
                       "public_key TEXT, "
                       "certificate TEXT)")
        conn.commit()
        conn.close()
    except (ValueError, TypeError) as e:
        raise DatabaseError(message=f"{e}")
