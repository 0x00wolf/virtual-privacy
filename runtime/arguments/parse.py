import os
import argparse
from runtime.VPRuntimeError import VPRuntimeError


MODES = ['client', 'server', 'database', 'generate_pki', 'encrypt', 'decrypt']
HOST_OPERATIONS = ['c2', 'ftp', 'chat']
ENCRYPTION_CHOICES = ['file', 'f', 'dir', 'd', 'path', 'p']
ENCRYPTION_ASSIGNMENTS = {
    'f': 'file',
    'd': 'dir',
    'p': 'path',
}
PKI_OPERATIONS = ['rsa', 'self-sign', 'ss', 'root-ca', 'ca', 'fast-gen', 'fg']
PKI_ASSIGNMENTS = {
    'ss': 'self-sign',
    'ca': 'root-ca',
    'fg': 'fast-gen',
}
DATABASE_OPERATIONS = [
    'add-key', 'ak', 'add-server', 'as', 'show-key', 'sk', 'show-keys',
    'show-server', 'ss', 'show-servers', 'show-tables', 'delete-key', 'dk',
    'delete-server', 'ds']
DATABASE_ASSIGNMENTS = {
    'ak': 'add-key',
    'as': 'add-server',
    'sk': 'show-key',
    'ss': 'show-server',
    'dk': 'delete-key',
    'ds': 'delete-server',
}


def parse():
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
        description="Virtual-Privacy"
                    "\nA Pythonic Swiss army knife for "
                    "conducting covert "
                    "communications over insecure networks in \nthe presence "
                    "of third parties, while maintaining "
                    "confidentiality, integrity, & authenticity.",
    )

    # Main runtime operating modes.
    modes = p.add_argument_group(title='OPERATING MODES')
    mode_group = modes.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        '--client', '-c',
        nargs='?',
        choices=HOST_OPERATIONS,
        default=None,
        metavar='OPERATION',
        help="[*] Connect to a VP server"
             "\n[-] Operations:"
             "\nc2            # Command & Control - send a reverse shell."
             "\nftp           # File Transfer - connect & download a file."
             "\nchat          # Chatroom - connect to a chatroom server."
             '\n'
             '\n[-] 4 Levels of encryption:'
             '\n1) Base64     # Base64 encoding (no credentials supplied).'
             '\n2) SSL        # TLSv1.3 encrypted communications'
             '\n              * Requires: Servers -crt'
             '\n3) VPP        # Virtual Privacy network security protocol'
             '\n              * Requires: A local -pr & a remote -pu'
             '\n4) VPP & SSL  # VPP wrapped in TLSv1.3'
             '\n              * Requires: A local -pr, signed -crt, & remote '
             "\n                          server's -pu.\n"
    )
    mode_group.add_argument(
        '--server', '-s',
        nargs='?',
        choices=HOST_OPERATIONS,
        default=None,
        metavar='OPERATION',
        help=
        '[*] Start a local VP server instance'
        '\n[-] Operations:'
        '\nc2            # Command & Control - receive a reverse shell. '
        '\nftp           # File Transfer - Host a file for download.'
        '\nchat          # Chatroom - Host a chatroom server.'
        '\n'
        '\n[-] 4 Levels of encryption:'
        '\n1) Base64     # Base64 encoding (no credentials supplied).'
        '\n2) SSL        # TLSv1.3 encrypted communications'
        '\n              * Requires: Local --private-key & signed -crt.'
        '\n3) VPP        # Virtual Privacy network security protocol.'
        '\n              * Requires: Local -pr & remote users RSA public keys'
        '\n                          stored in the database.'
        '\n4) VPP & SSL  # VPP wrapped in TLSv1.3'
        '\n              * Requires: A local -pr, signed -crt, & the -pu'
        '\n                          stored in the runtime SQL database.'
        '\n                          of any remote users who will connect.'
        '\n'
    )
    mode_group.add_argument(
        '--generate-pki', '-pki',
        nargs='?',
        choices=PKI_OPERATIONS,
        default=None,
        metavar='OPERATION',
        help=
        '[*] Generate public key infrastructure.'
        '\n# Default: self-sign'
        '\n[-] Operations:'
        '\nrsa              # Generate a new RSA key pair'
        '\n                 # Optional: Supply export paths for the public' 
        '\n                 # and private key with -pr & -pu'
        '\nself-sign | ss   # Create a self-signed X509 certificate'
        '\n                 * Requires: Local -pr & -crt export path.'
        '\nroot-ca | ca     # Interactive Public Key Infrastructure.'
        '\nfast-gen | fg    # Generate a --private-key & signed --certificate.'
        '\n                 * Optional: Export paths for -pr & -crt'
        '\n                 # Defaults: ./key.pem & ./cert.crt' 
        '\n'

    )
    mode_group.add_argument(
        '--encrypt', '-e',
        nargs='?',
        choices=ENCRYPTION_CHOICES,
        default=None,
        metavar='OPERATION',
        help='[*] VPP file encryption operations'
             '\n[-] Operations:'
             '\nfile | f    # Encrypt a --file-in | -fi'
             '\n            * Requires: -fi, -pu'
             '\n            # Optional signature : --private-key | -pr, '
             '\n            # Optional file out: -file-out | -fi'
             '\ndir | d     # Encrypt all of the files in a directory '
             '\n            # Non-recursive, does not encrypt files in '
             '\n              subdirectories.'
             '\n            * Requires: a directory path (-fi), -pr, and -pu.'
             '\npath | p    # Encrypt all of the files recursively from a '
             '\n              given path (file-in).'
             '\n            * Requires: a path to encrypt (-fi), -pr, and -pu.'
             '\n'
    )
    mode_group.add_argument(
        '--decrypt', '-d',
        nargs='?',
        choices=ENCRYPTION_CHOICES,
        default=None,
        metavar='OPERATION',
        help='[*] VPP file decryption operations'
             '\n[-] Operations:'
             '\nfile | f    # Decrypt a file (file-in) to a specified '
             '\n              export path (file-out), using the VP encryption'
             '\n            * Requires: -fi, -fo, -pr, -pu'
             '\n              protocol. '
             '\ndir | d     # Decrypt all of the files in a directory '
             '\n            # Non-recursive, does not encrypt files in '
             '\n              subdirectories.'
             '\n            * Requires: a directory path (-fi), -pr, and -pu.'
             '\npath | p    # Decrypt all of the files recursively from a '
             '\n              given path (file-in).'
             '\n            * Requires: a path to encrypt (-fi), -pr, and -pu.'
             '\n'
    )
    mode_group.add_argument(
        '--database', '-db',
        nargs='?',
        choices=DATABASE_OPERATIONS,
        default=None,
        metavar='OPERATION',
        help=
        '[*] Database operations'
        '\n[-] Operations:'
        '\nadd-key | ak       # Add a remote -pu to the SQL database.'
        '\n                   * Requires: Remote --public-key.'
        '\n                   * Optional: Set a nickname --target.'
        '\nadd-server | as    # Save connection information for a remote'
        '\n                     server in the SQL database.'
        '\n                   * Requires: --t (reference nickname), -ip, & -p.'
        '\n                   * Optional: A --public-key &/or --certificate.'
        '\nshow-key | sk      # Show a saved public key by ID or nickname.'
        '\n                   * Requires: --target (ID or nickname).'
        '\nshow-keys          # Display information for every stored key. '
        '\nshow-server | ss   # Display information about a stored server.'
        '\n                   * Requires: --target (nickname).'
        '\nshow-servers       # Display information for every stored server.'
        '\ndelete-key | dk    # Delete key based on its id number or nickname.'
        '\n                   * Requires: --target (ID or nickname).'
        '\ndelete-server      # Delete a server based selected via nickname.'
        '\n                   * Requires: --target (nickname).'
        '\n'
    )

    # Host configuration arguments
    hosts = p.add_argument_group(title='HOST CONFIGURATION')
    hosts.add_argument(
        '--host', '-ip',
        default='127.0.0.1',
        type=str,
        help="\n[*] Hostname or IPv4 address."
             "\n# Default: '127.0.0.1"
             "\n# For broadcast: '0.0.0.0'"
             "\n"
    )
    hosts.add_argument(
        '--port', '-p',
        default=1337,
        type=int,
        help="\n[*] Set the port. "
             "\n# Default: 1337"
             "\n# Evasion: Use SSL & port 443 to spoof HTTPS/DOH, 853 for DoT."
             "\n"
    )
    hosts.add_argument(
        '--private-key', '-pr',
        default=None,
        type=str,
        help="[*] Path to an RSA private key."
             "\n"
    )
    hosts.add_argument(
        '--public-key', '-pu',
        default=None,
        type=str,
        help="[*] Path to an RSA public key."
             "\n"
    )
    hosts.add_argument(
        '--certificate', '-crt',
        default=None,
        type=str,
        help="[*] Path to a signed x509 certificate."
             "\n"
    )
    hosts.add_argument(
        '--only-ssl', '-os',
        action='store_true',
        help="\n[*] Required for a server using SSL encryption without VPP."
             "\n"
    )
    hosts.add_argument(
        '--banner', '-b',
        default=None,
        type=str,
        help="[*] Set the banner message for a VP Chatroom server."
             "\n"
    )

    # File in & File out arguments
    fifo = p.add_argument_group(
        title='FILE-IN/FILE-OUT',
    )
    fifo.add_argument(
        '--file-in', '-fi',
        default=None,
        required=False,
        type=str,
        help="[*] Supply the path to a file."
             "\n"
    )
    fifo.add_argument(
        '--file-out', '-fo',
        default=None,
        required=False,
        type=str,
        help="[*] Supply the export path for a file."
             "\n"
    )
    db = p.add_argument_group(title='DATABASE OPTIONAL ARGUMENTS')
    db.add_argument(
        '--user', '-u',
        default='user',
        required=False,
        type=str,
        help="[*] Select a name to generate a new SQL database"
             "\n# Export path: './data/{USER}_database.db'"
             "\n"
    )
    db.add_argument(
        '--target', '-t',
        default=None,
        type=str,
        help="[*] Nickname for a target server or public key."
             "\n"
    )
    args = p.parse_args()

    # Expand operation acronyms
    if args.encrypt:
        if len(args.encrypt) == 1:
            args.encrypt = ENCRYPTION_ASSIGNMENTS[args.encrypt]
    if args.decrypt:
        if len(args.decrypt) == 1:
            args.decrypt = ENCRYPTION_ASSIGNMENTS[args.decrypt]
    if args.generate_pki:
        if len(args.generate_pki) == 2:
            args.generate_pki = PKI_ASSIGNMENTS[args.generate_pki]
    if args.database:
        if len(args.database) == 2:
            args.database = DATABASE_ASSIGNMENTS[args.database]

    # Handle file-in/file-out path requirements for FTP Host operations.
    if args.server == 'ftp':
        if not args.file_in:
            raise VPRuntimeError(
                message="Server operation FTP requires the path to a file in.")

    if args.client == 'ftp':
        if not args.file_out:
            raise VPRuntimeError(
                message="Client FTP operation requires a file out path.")

    # Set the mode to return.
    for _mode in MODES:
        if getattr(args, _mode):
            mode = _mode
            break

    # Set the operation to return.
    for _option in dir(args):
        if _option == mode:
            operation = getattr(args, _option)
            break

    # Remove underscores from returned mode & capitalize.
    mode = mode.replace('_', ' ')
    mode = mode.upper()
    print(f"[ ] Mode: {mode}")

    return mode, operation, args

