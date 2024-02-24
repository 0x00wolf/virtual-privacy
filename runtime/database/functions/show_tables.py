import sqlite3
from runtime.database.DatabaseError import DatabaseError


def show_tables(database_path):
    try:
        con = sqlite3.connect(database_path)
        cursor = con.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        for table in tables:
            table_name = table[0]
            print("Table: ", table_name)
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            for column in columns:
                column_name = column[1]
                print("Column: ", column_name)
            print()
        con.close()
    except (TypeError, ValueError) as e:
        raise DatabaseError(message=f"{e}")
