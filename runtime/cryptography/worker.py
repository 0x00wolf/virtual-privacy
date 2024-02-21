import os

from runtime.VPRuntimeError import VPRuntimeError
from crypter.CrypterError import CrypterError
import crypter.decrypt
import crypter.encrypt
import runtime


def worker(arguments):
    # Import necessary credentials
    credentials = runtime.credentials.factory(arguments)

    # ENCRYPTION
    if arguments.encrypt:
        # If not RSA public key throw error
        if not arguments.public_key:
            raise VPRuntimeError(
                message="Missing: --public-key | -pu"
                        "\n[ ] The path to an RSA public key is required for "
                        "VPP encryption."
                        "\n[ ] Optional: An RSA --private-key (-pr) for "
                        "signature authentication."
            )

        # ENCRYPT FILE
        if arguments.encrypt == 'file':
            if not arguments.file_in:
                raise VPRuntimeError(
                    message="Missing: --file-in, -fi"
                            "\n[ ] The path to a file is required for VPP "
                            "encryption.")
            if not arguments.file_out:
                arguments.file_out = arguments.file_in
            try:
                if credentials.private_key:
                    crypter.encrypt.signed_file(
                        file_in=arguments.file_in,
                        file_out=arguments.file_out,
                        public_key=credentials.public_key,
                        private_key=credentials.private_key,
                        verbose=True)
                else:
                    crypter.encrypt.file(file_in=arguments.file_in,
                                         file_out=arguments.file_out,
                                         public_key=credentials.public_key,
                                         verbose=True)
                print(f"[*] Operation complete")
            except CrypterError as e:
                print(f"[!] Error encrypting: {arguments.file_in}")
                raise VPRuntimeError(
                    message=f"{e}"
                )

        # ENCRYPT DIRECTORY
        elif arguments.encrypt == 'dir':
            if not arguments.file_in:
                raise VPRuntimeError(
                    message="Missing: --file-in | -fi"
                            "\n[ ] The path to the directory selected for VPP "
                            "encryption is required.")
            files_encrypted = 0
            print(arguments.file_in)
            root = os.path.abspath(arguments.file_in)
            files = [os.path.join(root, file) for file in os.listdir(root)]
            try:
                for file in files:
                    if os.path.isfile(file):
                        if not credentials.private_key:
                            crypter.encrypt.file(
                                file_in=file,
                                file_out=file,
                                public_key=credentials.public_key,
                                verbose=True)
                            files_encrypted += 1
                        else:
                            crypter.encrypt.signed_file(
                                file_in=file,
                                file_out=file,
                                public_key=credentials.public_key,
                                private_key=credentials.private_key,
                                verbose=True)
                            files_encrypted += 1
                print(f"[*] Operation complete"
                      f"\n[ ] Total files encrypted: {files_encrypted}")
            except CrypterError as e:
                print(f"[!] Failed to encrypt: {file}")
                raise VPRuntimeError(
                    message=f"{e}"
                )

        # ENCRYPT PATH
        elif arguments.encrypt == 'path':
            if not arguments.file_in:
                raise VPRuntimeError(
                    message="Missing: --file-in | -fi"
                            "\n[ ] VPP path encryption requires a "
                            "path to encrypt.")
            files_encrypted = 0
            files = []
            for _root, _dir, filenames in os.walk(arguments.file_in):
                root = os.path.abspath(_root)
                for filename in filenames:
                    files.append(os.path.join(root, filename))
            try:
                for _file in files:
                    if credentials.private_key:
                        crypter.decrypt.signed_file(
                            file_in=str(_file),
                            file_out=str(_file),
                            private_key=credentials.private_key,
                            public_key=credentials.public_key,
                            verbose=True)
                        files_encrypted += 1
                    else:
                        crypter.encrypt.file(
                            file_in=str(_file),
                            file_out=str(_file),
                            public_key=credentials.public_key,
                            verbose=True)
                        files_encrypted += 1
                print(f"[*] Operation complete")
                print(f"[ ] Total files encrypted: {files_encrypted}")
            except CrypterError as e:
                print(f"[!] Failed to encrypt file: {_file}")
                raise VPRuntimeError(
                    message=f"{e}"
                )

    # DECRYPTION
    if arguments.decrypt:
        # If not private key throw error
        if not arguments.private_key:
            raise VPRuntimeError(
                message="[!] Missing: RSA --private-key | -pr"
                        "\n[ ] Private key is required for file decryption."
                        "\n[ ] Optional: An RSA public key to verify a "
                        "signed file."
            )

        # DECRYPT FILE
        if arguments.decrypt == 'file':
            if not arguments.file_in:
                raise VPRuntimeError(
                    message="Missing: --file-in."
                            "\n[ ] The path to the encrypted file is required "
                            "for VPP decryption.")
            if not arguments.file_out:
                arguments.file_out = arguments.file_in
            try:
                if arguments.public_key:
                    crypter.decrypt.signed_file(
                        file_in=arguments.file_in,
                        file_out=arguments.file_out,
                        private_key=credentials.private_key,
                        public_key=credentials.public_key,
                        verbose=True)
                else:
                    crypter.decrypt.file(
                        file_in=arguments.file_in,
                        file_out=arguments.file_out,
                        private_key=credentials.private_key,
                        verbose=True)
            except CrypterError as e:
                print(f"[!] Failed to decrypt: {arguments.file_in}")
                raise VPRuntimeError(
                    message=f"{e}"
                )

        # DECRYPT DIRECTORY
        elif arguments.decrypt == 'dir':
            if not arguments.file_in:
                raise VPRuntimeError(
                    message="Missing: --file-in | -fi"
                            "\n[ ] The path to the encrypted directory is "
                            "required for VPP decryption.")
            files_decrypted = 0
            root = os.path.abspath(arguments.file_in)
            files = [os.path.join(root, file) for file in os.listdir(root)]
            for file in files:
                if os.path.isfile(file):
                    try:
                        if credentials.public_key:
                            crypter.decrypt.signed_file(
                                file_in=file,
                                file_out=file,
                                private_key=credentials.private_key,
                                public_key=credentials.public_key,
                                verbose=True)
                            print(f"[ ] File decrypted & good signature:"
                                  f" {file}")
                            files_decrypted += 1
                        else:
                            crypter.decrypt.file(
                                file_in=file,
                                file_out=file,
                                private_key=credentials.private_key,
                                verbose=True)
                            files_decrypted += 1
                    except CrypterError as e:
                        print(f"[!] Decryption error {e}")
            print(f"[*] Operation complete")
            print(f"[ ] Total files decrypted: "
                  f"{files_decrypted}"
                  )

        # DECRYPT PATH
        elif arguments.decrypt == 'path':
            if not arguments.file_in:
                raise VPRuntimeError(
                    message="Missing: --file-in | -fi"
                            "\n[ ] VPP path decryption requires a path to "
                            "decrypt.")
            files_decrypted = 0
            files = []
            for _root, _dir, filenames in os.walk(arguments.file_in):
                root = os.path.abspath(_root)
                for filename in filenames:
                    files.append(os.path.join(root, filename))
            for _file in files:
                if os.path.isfile(_file):
                    try:
                        if credentials.public_key:
                            crypter.decrypt.signed_file(
                                file_in=str(_file),
                                file_out=str(_file),
                                private_key=credentials.private_key,
                                public_key=credentials.public_key,
                                verbose=True)
                            files_decrypted += 1
                        else:
                            crypter.decrypt.file(
                                file_in=str(_file),
                                file_out=str(_file),
                                private_key=credentials.private_key,
                                verbose=True)
                            files_decrypted += 1
                    except CrypterError as e:
                        print(f"[!] Error decrypting file: {_file}")
                        print(f"[ ] Error: {e}")
            print(f"[*] Operation complete")
            print(f"[ ] Total files decrypted: "
                  f"{files_decrypted}"
                  )
