import runtime.database.functions
from runtime.database.DatabaseError import DatabaseError


def worker(arguments, database_path):
    try:
        # add key
        if arguments.database == 'add-key':
            if not arguments.public_key:
                raise VPRuntimeError(message="Operation requires an RSA public"
                                             " key to store in the database.")
            runtime.database.add_key(
                database_path=database_path,
                public_key=arguments.public_key,
                nickname=arguments.target)

        # add server
        elif arguments.database == 'add-server':
            if not arguments.host or not arguments.port or not arguments.target:
                raise VPRuntimeError(
                    message="Operation requires Host, port, and target "
                            "nickname.\n[ ] Certificate and RSA public key are"
                            " optional.")
            print(f"[*] Adding server {arguments.target} to "
                  f"{arguments.user.title()}'s SQL database: ")
            runtime.database.add_target(
                server_nickname=arguments.target,
                host=arguments.host,
                port=arguments.port,
                public_key=arguments.public,
                certificate=arguments.certificate,
                database_path=database_path)

        # show server
        elif arguments.database == 'show-server':
            if not arguments.target:
                raise VPRuntimeError(message="Operation requires a target "
                                             "ID or nickname.")
            print(f"[*] Displaying information for {arguments.target} in"
                  f" {arguments.user.title()}'s SQL database: ")
            runtime.database.show_target(server_nickname=arguments.target,
                                         database_path=database_path)

        # show servers
        elif arguments.database == 'show-servers':
            print(f"[*] Displaying all saved servers in "
                  f"{arguments.user.title()}'s SQL database: ")
            runtime.database.show_targets(database_path=database_path)

        # show key
        elif arguments.database == 'show-key':
            if not arguments.target:
                raise VPRuntimeError(
                    message="Operation requires a target ID or nickname.")
            runtime.database.show_key(database_path=database_path,
                                      target=arguments.target)

        # show keys
        elif arguments.database == 'show-keys':
            print(f"[*] Displaying stored public keys from "
                  f"{arguments.user.title()}'s SQL database")
            runtime.database.show_keys(database_path=database_path)

        # delete key
        elif arguments.database == 'delete-key':
            if not arguments.target:
                raise VPRuntimeError(message="Operation requires a target"
                                             " nickname or ID.")
            print(f"[*] Deleting key ID {arguments.target} from "
                  f"{arguments.user.title()}'s SQL database ")
            runtime.database.delete_key(
                database_path=database_path,
                key_id=int(arguments.target))

        # delete server
        elif arguments.database == 'delete-server':
            if not arguments.target:
                raise VPRuntimeError(message="Operation requires a target "
                                             "nickname or ID.")
            print(f"[*] Deleting server {arguments.target} from "
                  f"{arguments.user.title()}'s SQL database: ")
            runtime.database.delete_target(
                server_nickname=arguments.target,
                database_path=database_path)

        # show tables
        elif arguments.database == 'show-tables':
            print(f"[*] Displaying table meta data: ")
            runtime.database.show_tables(database_path)

        print('[*] Database operation successful.')

    except DatabaseError as e:
        print(f"[!] Database error: {e}")



