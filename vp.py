import crypter
import runtime
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
        rpaths = runtime.Paths(user=arguments.user)
        arguments = runtime.database.initialize(
            arguments=arguments,
            database_path=rpaths.user_database)

        if mode == 'CLIENT' or mode == 'SERVER':
            try:
                host = runtime.Host.factory(
                    mode=mode,
                    operation=operation,
                    database_path=rpaths.user_database,
                    arguments=arguments)
                host.run()
            except NetworkError as e:
                print(f"[!] Fatal error {e}")

        elif mode == 'GENERATE PKI':
            runtime.pki.factory(args=arguments)

        elif mode == 'ENCRYPT' or mode == 'DECRYPT':
            try:
                runtime.cryptography.worker(arguments=arguments)
            except CrypterError:
                print(f"[ ] Exiting...")

        elif mode == 'DATABASE':
            runtime.database.worker(arguments=arguments,
                                    database_path=rpaths.user_database)

    except (DatabaseError, VPRuntimeError, NetworkError, CrypterError) as e:
        print(f"[!] Fatal error: {e}")
        print('[ ] Exiting...')
        sys.exit()
    except KeyboardInterrupt:
        print(f"[ ] Exiting...")
        sys.exit()
