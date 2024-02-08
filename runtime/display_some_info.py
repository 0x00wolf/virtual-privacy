def display_some_info(arguments, credentials, database_path):
    print(f"mode: {arguments.mode}")
    print(f"operation: {arguments.operation}")
    print(f"host: {arguments.host}")
    print(f"port: {arguments.port}")
    if not credentials:
        return
    if credentials.public_key:
        print(f"public key: {credentials.public_key}")
    if credentials.private_key:
        print(f"private key: {credentials.private_key}")
    if credentials.certificate_crt:
        print(f"certificate path: {credentials.certificate_crt}")
    print(f"SQL database: {database_path}")
