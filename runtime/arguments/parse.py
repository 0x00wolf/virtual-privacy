import os
import argparse
from runtime.VPRuntimeError import VPRuntimeError


MODES = ['client', 'server', 'database', 'pki', 'rsa', 'encrypt', 'decrypt']
HOST_OPERATIONS = ['c2', 'ftp', 'chat']
PKI_OPERATIONS = ['self-sign', 'root-ca', 'fast-gen']
DATABASE_OPERATIONS = ['add-key', 'add-server', 'show-key', 'show-keys',
                       'show-server', 'show-servers', 'show-tables',
                       'delete-key', 'delete-server']


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
        description="A Pythonic Swiss army knife for conducting covert "
                    "communications over insecure networks in the "
                    "presence of third parties."
    )
    mode = p.add_argument_group(title='Operating modes')
    mode_group = mode.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        '--client', '-c',
        nargs='?',
        choices=HOST_OPERATIONS,
        default=None,
        metavar='OPERATION',
        help="# Connect to a VP server"
             "\nOperations:"
             "\nc2      # Command & Control - send a reverse shell."
             "\nftp     # File Transfer - connect & download a file."
             "\nchat    # Chatroom - connect to a chatroom server."
    )
    mode_group.add_argument(
        '--server', '-s',
        nargs='?',
        choices=HOST_OPERATIONS,
        default=None,
        metavar='OPERATION',
        help='# Start a local VP server instance'
             '\nOperations:'
             '\nc2      # Command & Control - receive a reverse shell. '
             '\nftp     # File Transfer - host a file for download.'
             '\nchat    # Chatroom - host a chatroom server.'
    )
    mode_group.add_argument(
        '--rsa-keypair', '-rsa',
        action='store_true',
        help='\n# Generate an RSA keypair'
             '\n# Optional: supply export paths for the private & public keys.'
             '\n'
    )
    mode_group.add_argument(
        '--generate-pki', '-pki',
        nargs='?',
        choices=PKI_OPERATIONS,
        default='self-sign',
        metavar='OPERATION',
        help='# Generate public key infrastructure.'
             '\n# Default: self-sign'
             '\nOperations:'
             '\nself-sign   # Create a self-signed X509 certificate'
             '\n            # Requires an Rsa private key: --private-key|-pr'
             '\n              & a certificate export path: --certificate|-crt.'
             '\nroot-ca     # Generate a root certificate authority, an RSA '
             '\n              keypair, & a signed X509 certificate.'
             '\nfast-gen    # Instantly generate an RSA private key & '
             '\n              self-signed X509 certificate to establish an '
             '\n              SSL encrypted connection.\n'

    )
    mode_group.add_argument(
        '--database', '-db',
        nargs='?',
        choices=DATABASE_OPERATIONS,
        default=None,
        metavar='OPERATION',
        help='# Database operations'
             '\nOperations:'
             '\nadd-key       # Add a remote RSA public key to the SQL '
             'database.'
             '\nadd-server    # Save connection information for a remote '
             'server in the SQL database.'
             '\nshow-key      # Show a key by id number (set id with --target)'
             '\nshow-keys     # Display all stored keys with ID numbers'
             '\nshow-server   # Display a stored server based on target '
             'nickname'
             '\nshow-servers  # Display all the information on stored servers'
             '\ndelete-key    # Delete a key based on id number'
             '\ndelete-server # Delete a server based on target nickname\n'
    )
    modes = p.add_argument_group()
    hosts = p.add_argument_group(title='Host configuration')
    hosts.add_argument(
        '--host', '-ip',
        default='127.0.0.1',
        type=str,
        help="\n# Hostname or IPv4 address."
             "\n# Default: '127.0.0.1"
             "\n# For broadcast: '0.0.0.0'\n"
    )
    hosts.add_argument(
        '--port', '-p',
        default=1337,
        type=int,
        help="\n# Set the port. "
             "\n# Default: 1337"
             "\n# Evasion: Use SSL & port 443 to spoof HTTPS/DOH, 853 for DoT."
             "\n# Default: 1337"
             "\n"
    )
    hosts.add_argument(
        '--private-key', '-pr',
        default=None,
        type=str,
        help="# Path to an RSA private key."
             "\n"
    )
    hosts.add_argument(
        '--public-key', '-pu',
        default=None,
        type=str,
        help="# Path to an RSA public key."
             "\n"
    )
    hosts.add_argument(
        '--certificate', '-crt',
        default=None,
        type=str,
        help="# Path to a signed x509 certificate."
             "\n"
    )
    hosts.add_argument(
        '--only-ssl', '-os',
        action='store_true',
        help="\n# Required for a server using SSL encryption without VPP."
             "\n"
    )
    hosts.add_argument(
        '--banner', '-b',
        default=None,
        type=str,
        help="# Set the banner message for a VP Chatroom server."
             "\n"
    )
    fifo = p.add_argument_group(
        title='File-in & file-out paths',
    )
    fifo.add_argument(
        '--file-in', '-fi',
        default=None,
        required=False,
        type=str,
        help="# Supply the path to a file."
             "\n"
    )
    fifo.add_argument(
        '--file-out', '-fo',
        default=None,
        required=False,
        type=str,
        help="# Supply the export path for a file."
             "\n"
    )
    db = p.add_argument_group(title='Database optional arguments')
    db.add_argument(
        '--user', '-u',
        default='user',
        required=False,
        type=str,
        help="# Select a name to generate a new SQL database"
             "\n# Export path: './data/{USER}_database.db'"
             "\n"
    )
    db.add_argument(
        '--target', '-t',
        default=None,
        type=str,
        help="# Nickname for a target server or public key."
             "\n"
    )
    args = p.parse_args()
    if args.file_in:
        if not os.path.isfile(args.file_in):
            raise VPRuntimeError(f"File-in not found: {args.file_in}")
    for _mode in MODES:
        if getattr(args, _mode):
            mode = _mode
            break
    for _option in dir(args):
        if _option == mode:
            operation = getattr(args, _option)
            break
    if args.server == 'ftp':
        if not args.file_in:
            raise VPRuntimeError(message=f"Server operation FTP requires the "
                                         f"path to a file in.")
    if args.client == 'ftp':
        if not args.file_out:
            raise VPRuntimeError(message=f"Client FTP operation requires a "
                                         f"file out path.")
    return mode, operation, args

