import crypter
import runtime
import network
import sys

HKR = '1  0  1\n1  1  0\n0  0  0'


if __name__ == '__main__':
    try:
        print(HKR)
        arguments = runtime.parse_arguments()
        rpaths = runtime.RuntimePaths(user=arguments.user)
        arguments = runtime.DatabaseManager.initialize(
            arguments=arguments,
            database_path=rpaths.user_database)
        credentials = runtime.CredentialFactory.work(arguments)
        runtime.display_some_info(
            arguments=arguments,
            credentials=credentials,
            database_path=rpaths.user_database)
        m = arguments.mode
        if m == 'client' or m == 'server':
            host = network.HostFactory.work(
                mode=arguments.mode,
                operation=arguments.operation,
                host=arguments.host,
                port=arguments.port,
                private_key=credentials.private_key,
                public_key=credentials.public_key,
                certificate_crt=credentials.certificate_crt,
                banner=arguments.banner,
                database_path=rpaths.user_database)
            host.run()
        elif m == 'database':
            runtime.DatabaseManager.work(
                arguments=arguments,
                database_path=rpaths.user_database)
        elif m == 'pki':
            crypter.pki.easy_infrastructure()
        elif m == 'rsa':
            crypter.rsa.key.interactive_keypair(
                private_key_path=arguments.private,
                public_key_path=arguments.public)
        elif m == 'encrypt' or m == 'decrypt':
            print('do something')
    except (KeyboardInterrupt, network.database.DatabaseError,
            runtime.VPRuntimeError) as e:
        print(f"[!] Fatal error: {e}")
        print('[ ] Exiting...')
        sys.exit()
