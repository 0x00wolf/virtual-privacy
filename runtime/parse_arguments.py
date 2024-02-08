import argparse


def parse_arguments():
    """
    Argument parser handles the command line arguments.

    Mode:
        *Required
        '--mode' MODE or '-m' MODE
        options: ['server', 's',
                  'client', 'c',
                  'pki',
                  'rsa',
                  'encrypt', 'e',
                  'decrypt', 'd']
    Options:
    """

    p = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="A Pythonic Swiss army knife for conducting covert "
                    "communications over untrusted networks in the presence "
                    "of third parties.",
        epilog=("\n[*] Example use:"
                "\n\n[-] Server:"
                "\n./virtualprivacy.py server --host 0.0.0.0 --port 1337 "
                "--private ./keys/local/myserver_private.pem --operation chat"
                "\n./virtualprivacy.py s -ip 0.0.0.0 -p 1337 -pr "
                "./keys/local/myserver_private.pem -op chat"
                "\n\n[-] Client:"
                "\n./virtualprivacy.py client --host 192.168.2.15 -p 1337 "
                "--private ./keys/local/username_private.pem --public "
                "./keys/remote/remoteserver_public.pem"
                "\n./virtualprivacy.py c -h 192.168.2.15 -p 1337 --pr "
                "./keys/local/username_private.pem --pu ./keys/remote/remote"
                "server_private.pem "
                "\n\n[-] Generate Public Key Infrastructure (PKI):"
                "\n./virtualprivacy.py pki  # new interactive public key "
                "infrastructure"
                "\n\n[-] Generate a new RSA key pair:"
                "\n./virtualprivacy.py rsa  # new RSA key pair. input export "
                "paths during "
                "runtime"
                "\n./virtualprivacy.py rsa -pr ./keys/local/newusername_"
                "private.pem -pu ./keys/local/newusername_public.pem"
                "\n\n[-] SQL database commands:"
                "\n./virtualprivacy.py database --operation add --name "
                "new_remote_client --public /path/to/new/remote/client_"
                "public.pem"
                "\n./virtualprivacy.py d -op del --name username_to_delete"
                "\n./virtualprivacy.py d -op show --name username # show "
                "users full entry"
                "\n./virtualprivacy.py d -op show --name all  # show all "
                "users"))
    p.add_argument(
        'mode',
        choices=['server', 's', 'client', 'c', 'pki', 'rsa',
                 'encrypt', 'e', 'decrypt', 'd', 'database', 'db'],
        help=(
            "[*] MODE:"
            "\n[-] server, s        Start running a VP server"
            "\n[-] client, c        Connect to a VP server as a client"
            "\n[-] pki              Generate public key infrastructure (PKI)"
            "\n[-] rsa              Generate an RSA keypair, password optional"
            "\n[-] encrypt, e       Encrypt a file with the VP protocol"
            "\n[-] decrypt, d       Decrypt a file with the with VP protocol"
            "\n[-] database, db     Manage the local server's SQL database"
            "\n---"
        )
    )
    p.add_argument(
        '--host', '-ip',
        default='127.0.0.1',
        type=str,
        help="[-] Set the remote host or broadcast address.\n"
             "[-] Default: '127.0.0.1\n"
             "[-] Broadcast: '0.0.0.0'"
             "\n---"
    )
    p.add_argument(
        '--port', '-p',
        default=443,
        type=int,
        help="\n[-] Set the remote or local port. "
             "\n[-] Evasion: Use 443 to spoof HTTPS/DoH, or 853 to spoof DoT. "
             "Using --tsl (-tsl)."
             "\n[-] Default: 1337"
             "\n---"
    )
    p.add_argument(
        '--operation', '-op',
        default='chat',
        type=str,
        help="[-] Selects an operating mode, for hosts & servers, "
             "or selects a database operation."
             "\n[-] Default: chat"
             "\n[-] server types: chat, ftp, c2, nc"
             "\n[-] server database operations: add-user, show-user, "
             "show-users, delete-user"
             "\n[-] client database operations: add-target, show-target, "
             "show-targets, delete-target, show-tables"
    )
    p.add_argument(
        '--private', '-pr',
        default=None,
        type=str,
        help="[-] Set the path to a local RSA private key."
             "\n---"
    )
    p.add_argument(
        '--public', '-pu',
        default=None,
        type=str,
        help="[-] Set the path to an RSA public key."
             "\n---"
    )
    p.add_argument(
        '--certificate', '-crt',
        default=None,
        type=str,
        help="[-] For TLS, set the path to a server's signed-certificate or "
             "the root CA certificate for a client."
             "\n---"
    )
    p.add_argument(
        '--file-in', '-fi',
        default=None,
        required=False,
        type=str,
        help="\n[-] Supply the path to a file."
             "\n---"
    )
    p.add_argument(
        '--file-out', '-fo',
        default=None,
        required=False,
        type=str,
        help="[-] Supply the export path for a file."
             "\n---"
    )
    p.add_argument(
        '--user', '-u',
        default='user',
        required=False,
        type=str,
        help="[-] Sets the database name for a SQL database for clients and "
             "known servers."
    )
    p.add_argument(
        '--banner', '-b',
        default=None,
        type=str,
        help="[-] Set the banner message for client's connecting to a "
             "VP-Server."
    )
    p.add_argument(
        '--target', '-t',
        default=None,
        type=str,
        help="[-] Sets the target server or target nickname for database "
             "(operations).")
    args = p.parse_args()
    abbreviations = {'s': 'server',
                     'c': 'client',
                     'e': 'encrypt',
                     'd': 'decrypt',
                     'db': 'database'}
    if len(args.mode) <= 2:
        args.mode = abbreviations[args.mode]
    return args

