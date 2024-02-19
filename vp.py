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
        arguments = runtime.database_operations.initialize(
            arguments=arguments,
            database_path=rpaths.user_database)

        if mode == 'CLIENT' or mode == 'SERVER':
            try:
                host = runtime.host_factory(
                    mode=mode,
                    operation=operation,
                    database_path=rpaths.user_database,
                    arguments=arguments)
                host.run()
            except NetworkError as e:
                print(f"[!] Fatal error {e}")

        elif mode == 'RSA KEYPAIR':
            crypter.rsa.key.interactive_keypair(
                private_key_path=arguments.private_key,
                public_key_path=arguments.public_key)

        elif mode == 'GENERATE PKI':
            runtime.crypto_functions.generate_pki(arguments=arguments)

        elif mode == 'ENCRYPT' or mode == 'DECRYPT':
            try:
                runtime.crypto_functions.worker(arguments=arguments)
            except CrypterError:
                print(f"[ ] Exiting...")
        elif mode == 'DATABASE':
            runtime.database_operations.worker(
                arguments=arguments,
                database_path=rpaths.user_database)

    except (DatabaseError, VPRuntimeError, NetworkError, CrypterError) as e:
        print(f"[!] Fatal error: {e}")
        print('[ ] Exiting...')
        sys.exit()
    except KeyboardInterrupt:
        print(f"[ ] Exiting...")
        sys.exit()
