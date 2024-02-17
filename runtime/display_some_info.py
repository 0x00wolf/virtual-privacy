def display_some_info(mode, arguments, credentials, database_path):
    priv_key = credentials.private_key
    pub_key = credentials.public_key
    priv_pem = arguments.private_keyds
    cert = credentials.certificate_crt

    print(f"[ ] Host: {arguments.host}")
    print(f"[ ] Port: {arguments.port}")

    if not credentials:
        return
    if pub_key:
        print(f"[ ] Public key: {pub_key}")
    if priv_key:
        print(f"[ ] Private key: {priv_key}")
    if cert:
        print(f"[ ] Certificate path: {cert}")

    if mode == 'server':
        if priv_key and not cert:
            print("[ ] Encryption: VP-Protocol")
        elif priv_key and cert:
            print("[ ] Encryption: SSL & VP-Protocol")
        elif priv_pem and not priv_key and cert:
            print("[ ] Encryption: SSL & Base64")
        elif not priv_pem and not priv_key and not cert:
            print("[ ] Encryption: Base64")

    elif mode == 'client':
        if priv_key and pub_key and cert:
            print("[ ] Encryption: SSL & VP-Protocol")
        elif priv_key and pub_key and not cert:
            print("[ ] Encryption: VP-Protocol")
        elif not priv_key and not pub_key and cert:
            print("[ ] Encryption: SSL & Base64")
        elif not priv_key and not pub_key and not cert:
            print("[ ] Encryption: Base64")

    if mode == 'server' or mode == 'client':
        print(f"[ ] SQL database: {database_path}")
    if arguments.file_in:
        print(f"[ ] File in: {arguments.file_in}")
    if arguments.file_out:
        print(f"[ ] File export path: {arguments.file_out}")
