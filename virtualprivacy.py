import crypter
import runtime
import network
import sys

from crypter.CrypterError import CrypterError
from network.NetworkError import NetworkError
from runtime.database.DatabaseError import DatabaseError
from runtime.VPRuntimeError import VPRuntimeError

HKR = '1  0  1\n1  1  0\n0  0  0'

if __name__ == '__main__':
    try:
        print(HKR)
        mode, operation, arguments = runtime.arguments.parse()
        rpaths = runtime.RuntimePaths(user=arguments.user)
        arguments = runtime.DatabaseManager.initialize(
            arguments=arguments,
            database_path=rpaths.user_database)
        print(f"[ ] Mode: {mode.title()}")
        print(f"[ ] Operation: {operation.title()}")
        if arguments.client or arguments.server:
            try:
                host = network.host_factory(
                    mode=mode,
                    operation=operation,
                    database_path=rpaths.user_database,
                    arguments=arguments)
                host.run()
            except NetworkError as e:
                print(f"[!] Fatal error {e}")
        elif arguments.database:
            runtime.DatabaseManager.work(
                arguments=arguments,
                database_path=rpaths.user_database)
        elif arguments.pki:
            if arguments.pki == 'self-sign' and arguments.private \
                    and arguments.certificate:
                print(f"[*] Exporting self-signed certificate to: "
                      f"{arguments.certificate}")
                crypter.pki.self_sign(
                    private_key_path=arguments.private,
                    certificate_export_path=arguments.certificate)
            elif operation == 'ca':
                crypter.pki.easy_infrastructure()
            else:
                print(f"[!] Invalid PKI operation."
                      f"\n\n[*] To self sign provide a private key and a "
                      f"certificate export path:"
                      f"\npython virtualprivacy.py pki -crt "
                      f"EXPORT/CERT.crt -pr PATH/KEY.pem"
                      f"\n\n[*] You can generate public key "
                      f"infrastructure interactively (a root Certificate "
                      f"Authority & a signed domain certificate) by setting "
                      f"the operation to 'ca':"
                      f"\npython virtualprivacy.py pki -op ca")
        elif mode == 'rsa':
            crypter.rsa.key.interactive_keypair(
                private_key_path=arguments.private,
                public_key_path=arguments.public)
        elif mode == 'encrypt' or mode == 'decrypt':
            print('do something')
    except (DatabaseError, VPRuntimeError, NetworkError, CrypterError) as e:
        print(f"\n[!] Fatal error: {e}")
        print('[ ] Exiting...')
        sys.exit()
    except KeyboardInterrupt:
        print(f"\n[ ] Exiting...")
        sys.exit()
