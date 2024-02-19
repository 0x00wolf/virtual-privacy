import sqlite3
import sys
import os

import runtime.database
from runtime.database.DatabaseError import DatabaseError


def initialize(arguments, database_path):
    runtime.database.create_database(database_path)
    if arguments.client and arguments.target:
        (arguments.target_name,
         arguments.host,
         arguments.port,
         arguments.public,
         arguments.certificate) = runtime.database.retrieve_target(
            target_name=arguments.target,
            database_path=database_path)
    return arguments


def worker(arguments, database_path):
    try:
        if arguments.database == 'add-key':
            runtime.database.add_key(
                database_path=database_path,
                public_key=arguments.public_key,
                nickname=arguments.target)
        elif arguments.database == 'show-key':
            runtime.database.show_key(database_path=database_path,
                                      target=arguments.target)
        elif arguments.database == 'show-keys':
            print(f"[*] Displaying stored public keys from "
                  f"{arguments.user.title()}'s SQL database")
            runtime.database.show_keys(
                database_path=database_path)
        elif arguments.database == 'delete-key':
            print(f"[*] Deleting key ID {arguments.target} from "
                  f"{arguments.user.title()}'s SQL database ")
            runtime.database.delete_key(
                database_path=database_path,
                key_id=int(arguments.target))
        elif arguments.database == 'add-server':
            print(f"[*] Adding server {arguments.target} to "
                  f"{arguments.user.title()}'s SQL database: ")
            runtime.database.add_target(
                server_nickname=arguments.target,
                host=arguments.host,
                port=arguments.port,
                public_key=arguments.public,
                certificate=arguments.certificate,
                database_path=database_path)
        elif arguments.database == 'show-server':
            print(f"[*] Displaying information for {arguments.target} in"
                  f" {arguments.user.title()}'s SQL database: ")
            runtime.database.show_target(
                server_nickname=arguments.target,
                database_path=database_path)
        elif arguments.database == 'show-servers':
            print(f"[*] Displaying all saved servers in "
                  f"{arguments.user.title()}'s SQL database: ")
            runtime.database.show_targets(
                database_path=database_path)
        elif arguments.database == 'delete-server':
            print(f"[*] Deleting server {arguments.target} from "
                  f"{arguments.user.title()}'s SQL database: ")
            runtime.database.delete_target(
                server_nickname=arguments.target,
                database_path=database_path)
        elif arguments.database == 'show-tables':
            print(f"[*] Displaying table meta data: ")
            runtime.database.show_tables(database_path)
        print('[*] Database operation successful.')
    except DatabaseError as e:
        print(f"[!] Database error: {e}")
