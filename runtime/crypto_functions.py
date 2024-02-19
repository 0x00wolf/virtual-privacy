import os

import runtime
import crypter.decrypt
import crypter.encrypt
from crypter.CrypterError import CrypterError
import crypter.pki


def generate_pki(arguments):
    if arguments.generate_pki == 'self-sign':
        print(f"[*] Exporting self-signed certificate to: "
              f"{arguments.certificate}")
        crypter.pki.self_sign(
            private_key_path=arguments.private_key,
            certificate_export_path=arguments.certificate)
    elif arguments.generate_pki == 'root-ca':
        crypter.pki.easy_infrastructure()
    elif arguments.generate_pki == 'fast-gen':
        crypter.pki.gen_cert_key(
            private_key=arguments.private_key,
            certificate=arguments.certificate)


def worker(arguments):
    credentials = runtime.credential_factory(arguments)

    if arguments.encrypt:
        if arguments.encrypt == 'file':
            crypter.encrypt.signed_file(file_in=arguments.file_in,
                                        file_out=arguments.file_out,
                                        public_key=credentials.public_key,
                                        private_key=credentials.private_key,
                                        verbose=True)
            print(f"[ ] File encrypted: {file}")
            print(f"[*] Operation complete")

        elif arguments.encrypt == 'dir':
            files_encrypted = 0
            files = [f for f in os.listdir(arguments.file_in) if
                     os.path.isfile(os.path.join(arguments.file_in, f))]
            for file in files:
                try:
                    crypter.encrypt.signed_file(
                        file_in=file,
                        file_out=file,
                        public_key=credentials.public_key,
                        private_key=credentials.private_key,
                        verbose=True
                    )
                    print(f"[ ] File encrypted: {file}")
                    files_encrypted += 1
                except CrypterError as e:
                    print(f"[!] Failed to encrypt file: {file}"
                          f"\n[ ] Error: {e}")
                    cont = input(f"[*] Continue encryption process? (y/n)"
                                 f"[>] Selection: ")
                    if cont == 'n':
                        raise CrypterError
            for file in files:
                os.rename(file, f"{file}.vpp")
            print(f"[*] Operation complete"
                  f"\n[ ] Total files encrypted: {files_encrypted}")

        elif arguments.encrypt == 'path':
            files_encrypted = 0
            files = []
            for root, _, filenames in os.walk(arguments.file_in):
                for filename in filenames:
                    files.append(os.path.join(root, filename))
            for _file in files:
                if _file.endswith('.vpp'):
                    print(f"[ ] Decrypting: {_file}")
                    try:
                        crypter.decrypt.signed_file(
                            file_in=str(_file),
                            file_out=str(_file),
                            private_key=credentials.private_key,
                            public_key=credentials.public_key,
                            verbose=True
                        )
                        print(f"[ ] File encrypted: {_file}")
                        files_encrypted += 1
                    except CrypterError as e:
                        cont = input(f"[!] Failed to encrypt file: {_file}"
                                     f"\n[ ] Error: {e}"
                                     f"\n[*] Continue? (y/n)"
                                     f"\n[>] Selection: ")
                        if cont == 'n':
                            raise CrypterError(message=f"{e}")
            print(f"[*] Operation complete")
            print(f"[ ] Total files encrypted: {files_encrypted}")

    if arguments.decrypt:
        if arguments.decrypt == 'file':
            crypter.decrypt.signed_file(
                file_in=arguments.file_in,
                file_out=arguments.file_out,
                private_key=credentials.private_key,
                public_key=credentials.public_key,
                verbose=True)

        elif arguments.decrypt == 'dir':
            files_decrypted = 0
            files = [f for f in os.listdir(arguments.file_in) if
                     os.path.isfile(os.path.join(arguments.file_in, f))]
            for file in files:
                if file.endswith('.vpp'):
                    print(f"[ ] Decrypting: {file}")
                    try:
                        crypter.decrypt.signed_file(
                            file_in=file,
                            file_out=file,
                            private_key=credentials.private_key,
                            public_key=credentials.public_key,
                            verbose=True
                        )
                        print(f"[ ] File decrypted: {file}")
                        files_decrypted += 1
                    except CrypterError as e:
                        cont = input(f"[!] Error decrypting file: {_file}"
                                     f"\n[ ] Error: {e}"
                                     f"\n[ ] Continue decryption process? ("
                                     f"y/n)\n[>] Selection: ")
                        if cont == 'n':
                            raise CrypterError
            print(f"[*] Operation complete")
            print(f"[ ] Total files decrypted: {files_decrypted}")

        elif arguments.decrypt == 'path':
            files_decrypted = 0
            files = []
            for root, _, filenames in os.walk(arguments.file_in):
                for filename in filenames:
                    files.append(os.path.join(root, filename))
            for _file in files:
                if _file.endswith('.vpp'):
                    print(f"[ ] Decrypting: {_file}")
                    try:
                        crypter.decrypt.signed_file(
                            file_in=str(_file),
                            file_out=str(_file),
                            private_key=credentials.private_key,
                            public_key=credentials.public_key,
                            verbose=True)
                        print(f"[ ] File decrypted: {file}")
                        files_decrypted += 1
                    except CrypterError as e:
                        cont = input(f"[!] Error decrypting file: {_file}"
                                     f"\n[ ] Error {e}"
                                     f"\n[ ] Continue? (y/n)"
                                     f"\n[>] Selection: ")
                        if cont == 'n':
                            raise CrypterError
            print(f"[*] Operation complete")
            print(f"[ ] Total files decrypted: {files_decrypted}")
