from getpass import getpass
import os

import crypter.rsa.key
from crypter.CrypterError import CrypterError
from runtime.VPRuntimeError import VPRuntimeError
from runtime.credentials.Credentials import Credentials


def factory(args) -> Credentials:
    """
    The credential factory identifies the required runtime credentials and
    attempts to import them, either successfully returning any necessary
    imported RSA keys for the runtime operation.

    Returns:
        Credentials (Class): Comprised of the following class instance
        variables:
        public_key (RSA.RsaKey | None): The receiver's RSA public key (
        server's track foreign public keys with the user database).
        private_key (RSA.RsaKey | None): The local RSA private key.
        credential_crt (str | None): The path to the root CA certificate,
        or the local server's signed-certificate.
    """
    try:
        # import keys:
        if args.target:
            public_key = crypter.rsa.key.load_key(
                pem_string=args.public_key)  # Takes a PEM string from memory
        elif args.public_key:
            public_key = crypter.rsa.key.load_key(
                pem_path=args.public_key)    # Takes the path to a PEM key
        else:
            public_key = None
        if args.private_key and not args.only_ssl:
            with open(args.private_key, 'r') as f:
                data = f.read()
            if 'ENCRYPTED' in data:
                password = getpass("[>] Password: ")
                private_key = crypter.rsa.key.load_key(
                    pem_path=args.private_key,
                    password=password)
            else:
                private_key = crypter.rsa.key.load_key(
                    pem_path=args.private_key)
        else:
            private_key = None
        if args.certificate:
            if not os.path.isfile(args.certificate):
                raise VPRuntimeError(f"File not found: "
                                     f"{args.certificate}")
        return Credentials(private_key=private_key,
                           public_key=public_key,
                           certificate_crt=args.certificate)
    except (CrypterError, FileNotFoundError) as e:
        raise VPRuntimeError(message=f"{e}")
