import sqlite3
from network.database.DatabaseError import DatabaseError


def create_database(database_path):
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        # Create the users table if it doesn't exist
        cursor.execute("CREATE TABLE IF NOT EXISTS users "
                       "(username TEXT, "
                       "rsa_public_key TEXT)")
        # Create the targets table if it doesn't exist
        cursor.execute("CREATE TABLE IF NOT EXISTS targets "
                       "(target_name TEXT PRIMARY KEY, "
                       "host TEXT, "
                       "port INTEGER, "
                       "public_key TEXT, "
                       "certificate TEXT)")
        conn.commit()
        conn.close()
    except (ValueError, TypeError) as e:
        raise DatabaseError(message=f"{e}")
