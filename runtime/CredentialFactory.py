import json

import crypter.rsa.key
from runtime.Credentials import Credentials
from crypter.CrypterError import CrypterError
from runtime.VPRuntimeError import VPRuntimeError


class CredentialFactory:
    @staticmethod
    def work(args) -> Credentials:
        """
        The credential factory identifies the required runtime credentials and
        attempts to import them, either successfully returning any necessary
        imported RSA keys for the runtime operation.

        Returns:
            public_key (RSA.RsaKey | None): The receiver's RSA public key (
            server's track foreign public keys with the user database).
            private_key (RSA.RsaKey | None): The local RSA private key.
            credential_crt (str | None): The path to the root CA certificate,
            or the local server's signed-certificate.
        """

        mode = args.mode
        if mode != 'server' or mode != 'client':
            return Credentials(private_key=None,
                               public_key=None,
                               certificate_crt=None)
        # SERVER
        if mode == 'server':
            if args.public:
                public_pem = args.public
            else:
                public_pem = None
            if args.private:
                private_pem = args.private
            else:
                private_pem = None
            # handle TLS
            if args.certificate:
                certificate_crt = args.certificate
            else:
                certificate_crt = None
        # CLIENT
        if mode == 'client':
            # client: public key
            if args.public:
                public_pem = args.public
            else:
                public_pem = None
            # client: private key
            if args.private:
                private_pem = args.private
            else:
                private_pem = None
            # HANDLE TLS
            if args.certificate:
                certificate_crt = args.certificate
            else:
                certificate_crt = None

        # IMPORT KEYS

        try:
            if args.target:
                public_key = crypter.rsa.key.load_key(
                    pem_string=args.public)
            elif public_pem:
                public_key = crypter.rsa.key.load_key(
                    pem_path=args.public)
        except CrypterError as e:
            raise VPRuntimeError(message=f"{e}")
        try:
            if private_pem:
                with open(private_pem, 'r') as f:
                    data = f.read()
                if 'ENCRYPTED' in data:
                    password = crypter.rsa.key.get_password()
                    private_key = crypter.rsa.key.load_key(
                        pem_path=private_pem,
                        password=password)
            else:
                private_key = crypter.rsa.key.load_key(
                    pem_path=private_pem)
        except CrypterError as e:
            raise VPRuntimeError(message=f"{e}")
        if certificate_crt:
            if not os.path.isfile(certificate_crt):
                raise VPRuntimeError(f"File not found: {certificate_crt}")
        else:
            pass
        return Credentials(private_key=private_key,
                           public_key=public_key,
                           certificate_crt=certificate_crt)
