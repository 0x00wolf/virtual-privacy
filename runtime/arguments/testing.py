import argparse

def main():
    # Step 2: Create an instance of ArgumentParser
    parser = argparse.ArgumentParser()

    # Step 3: Define the positional arguments for each mode
    host_choices = ['c2', 'ftp', 'chat']
    database_choices = ['add-key', 'add-server', 'show-key', 'show-keys', 'show-server', 'show-servers', 'show-tables', 'delete-key', 'delete-server']
    pki_choices = ['self-sign', 'root-ca', 'fast-gen']
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument('--server', '-s', nargs='?', choices=host_choices, default=None, help='Required operation for server mode')
    mode_group.add_argument('--client', '-c',  nargs='?', choices=host_choices, default=None, help='Required operation for client mode')
    mode_group.add_argument('--database', '-db', nargs='?', choices=database_choices, default=None, help='Required operation for database mode')
    mode_group.add_argument('-pki',  nargs='?', choices=pki_choices, default='self-sign', help='Optional for pki mode. Default: self-sign')
    mode_group.add_argument('-rsa', action='store_true', help='Generate an RSA keypair')
    # Step 4: Set the required mode using add_mutually_exclusive_group
    # Step 5: Parse the arguments
    args = parser.parse_args()

    # Do something based on the selected mode and positional arguments
    if args.server:
        print("Server mode selected with positional argument:", args.server_positional_arg)
    elif args.client:
        print("Client mode selected with positional argument:", args.client_positional_arg)
    elif args.database:
        print("Database mode selected with positional argument:", args.database_positional_arg)
    elif args.encrypt:
        print("Encrypt mode selected")
    elif args.decrypt:
        print("Decrypt mode selected")
    elif args.rsa:
        print("RSA mode selected")
    elif args.pki:
        print("PKI mode selected with positional argument:", args.pki_positional_arg)

if __name__ == '__main__':
    main()

