import sqlite3
import sys
import os

import network.database
from network.database.DatabaseError import DatabaseError


class DatabaseManager:
    @staticmethod
    def initialize(arguments, database_path):
        network.database.create_database(database_path)
        if arguments.mode != 'database' and arguments.target:
            (arguments.target_name,
             arguments.host,
             arguments.port,
             arguments.public,
             arguments.certificate) = network.database.retrieve_target(
                target_name=arguments.target,
                database_path=database_path)
        return arguments

    @staticmethod
    def work(arguments, database_path):
        print(f"[*] Database operation: {arguments.operation}")
        try:
            if arguments.operation == 'add-user':
                print('add')
                network.database.add_user(database_path=database_path,
                                          username=arguments.target,
                                          rsa_public_key=arguments.public)
            elif arguments.operation == 'show-user':
                print(f"[*] Displaying user info for {arguments.target} from"
                      f" {arguments.user.title()}'s SQL "
                      f"database: ")
                network.database.show_user(database_path=database_path,
                                           username=arguments.target)
            elif arguments.operation == 'show-users':
                print(f"[*] Displaying all user's in {arguments.user.title()}'s "
                      f"SQL "
                      f"database:")
                network.database.show_users(database_path=database_path)
            elif arguments.operation == 'delete-user':
                print(f"[*] Deleting {arguments.target} from "
                      f"{arguments.user.title()}'s SQL database: ")
                network.database.delete_user(database_path=database_path,
                                             username=arguments.target)
            elif arguments.operation == 'add-server':
                print(f"[*] Adding server {arguments.target} to "
                      f"{arguments.user.title()}'s SQL database: ")
                network.database.add_target(server_nickname=arguments.target,
                                            host=arguments.host,
                                            port=arguments.port,
                                            public_key=arguments.public,
                                            certificate=arguments.certificate,
                                            database_path=database_path)
            elif arguments.operation == 'show-server':
                print(f"[*] Displaying information for {arguments.target} in"
                      f" {arguments.user.title()}'s SQL database: ")
                network.database.show_target(server_nickname=arguments.target,
                                             database_path=database_path)
            elif arguments.operation == 'show-servers':
                print(f"[*] Displaying all saved servers in "
                      f"{arguments.user.title()}'s SQL database: ")
                network.database.show_targets(database_path=database_path)
            elif arguments.operation == 'delete-server':
                print(f"[*] Deleting server {arguments.target} from "
                      f"{arguments.user.title()}'s SQL database: ")
                network.database.delete_target(server_nickname=arguments.target,
                                               database_path=database_path)
            elif arguments.operation == 'show-tables':
                print(f"[*] Displaying table meta data: ")
                network.database.show_tables(database_path)
            print('[*] Database operation successful.')
        except DatabaseError as e:
            print(f"[!] Database error: {e}")