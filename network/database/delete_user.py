import sqlite3
from network.database.DatabaseError import DatabaseError


def delete_user(username, database_path):
    try:
        con = sqlite3.connect(database_path)
        cur = con.cursor()
        # Check if the username is valid
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cur.fetchone()
        if user:
            confirm = input(f"[?] Are you sure you want to delete user "
                            f"<{username}>? "
                            f"\n[>] (y/n): ")
            if confirm.lower() == 'y':
                cur.execute("DELETE FROM users WHERE username = ?", (username,))
                con.commit()
                print(f"[*] User <{username}> entry was successfully removed "
                      f"from the SQL database @ {database_path}")
            else:
                print("[*] Operation canceled.")
        else:
            print(f"[!] User <{username}> does not exist...")
        con.close()
    except (ValueError, TypeError) as e:
        raise DatabaseError(message=f"{e}")
