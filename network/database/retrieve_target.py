import sqlite3
from network.database.DatabaseError import DatabaseError


def retrieve_target(target_name, database_path):
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute("SELECT target_name, host, port, public_key, "
                       "certificate "
                       "FROM targets WHERE target_name = ? ", (target_name,))
        row = cursor.fetchone()
        conn.close()
        if row:
            target_name = row[0]
            host = row[1]
            port = row[2]
            public_key = row[3]
            certificate = row[4]
            return target_name, host, port, public_key, certificate
        else:
            return None
    except (ValueError, TypeError) as e:
        raise DatabaseError(message=e)
