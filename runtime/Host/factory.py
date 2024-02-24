from Crypto.PublicKey import RSA

import network.Host
import runtime.credentials
from runtime.VPRuntimeError import VPRuntimeError
from runtime.Host.display_info import display_info


def factory(mode, operation, arguments, database_path):
    mode = mode.lower()
    operation = operation.lower()
    host = arguments.host
    port = arguments.port
    banner = arguments.banner
    target = arguments.target
    file_in = arguments.file_in
    file_out = arguments.file_out
    private_pem = arguments.private_key
    public_pem = arguments.public_key
    only_ssl = arguments.only_ssl
    credentials = runtime.credentials.factory(arguments)
    private_key: RSA.RsaKey = credentials.private_key
    public_key: RSA.RsaKey = credentials.public_key
    certificate_crt: str = credentials.certificate_crt

    display_info(
        mode=mode,
        arguments=arguments,
        credentials=credentials,
        database_path=database_path)

    if operation == 'chat':
        if mode == 'server':
            if not banner:
                banner = 'Welcome to the AOL chatroom for spies!'
            if certificate_crt and private_key:
                return network.Host.ChatVPPSSL.Server(
                    host=host,
                    port=port,
                    banner=banner,
                    private_key=private_key,
                    database_path=database_path,
                    certificate=certificate_crt,
                    private_pem=private_pem
                )
            elif not certificate_crt and private_key:
                return network.Host.ChatVPP.Server(
                    host=host,
                    port=port,
                    banner=banner,
                    private_key=private_key,
                    database_path=database_path
                )
            elif certificate_crt and private_pem and not private_key:
                return network.Host.ChatSSL.Server(
                    host=host,
                    port=port,
                    banner=banner,
                    certificate=certificate_crt,
                    private_pem=private_pem
                )
            elif not certificate_crt and not private_pem and not public_pem:
                return network.Host.ChatB64.Server(
                    host=host,
                    port=port,
                    banner=banner
                )
            else:
                raise VPRuntimeError(
                    message="Missing or additional arguments provided for "
                            "Chatroom server operation.")
        elif mode == 'client':
            if certificate_crt and public_key and private_key:
                return network.Host.ChatVPPSSL.Client(
                    host=host,
                    port=port,
                    private_key=private_key,
                    public_key=public_key,
                    certificate=certificate_crt)
            elif not certificate_crt and public_key and private_key:
                return network.Host.ChatVPP.Client(
                    host=host,
                    port=port,
                    private_key=private_key,
                    public_key=public_key)
            elif certificate_crt and not private_key and not private_key:
                return network.Host.ChatSSL.Client(
                    host=host,
                    port=port,
                    certificate=certificate_crt
                )
            elif not certificate_crt and not private_pem and not public_pem:
                return network.Host.ChatB64.Client(
                    host=host,
                    port=port
                )
            else:
                raise VPRuntimeError(
                    message="Missing or additional arguments for "
                            "Chatroom client operation.")
    elif operation == 'ftp':
        if mode == 'server':
            if file_in and certificate_crt and private_key and not only_ssl:
                return network.Host.FTPVPPSSL.Server(
                    host=host,
                    port=port,
                    file_in=file_in,
                    private_key=private_key,
                    certificate=certificate_crt,
                    private_pem=private_pem,
                    database_path=database_path
                )
            elif file_in and not certificate_crt and private_key:
                return network.Host.FTPVPP.Server(
                    host=host,
                    port=port,
                    file_in=file_in,
                    private_key=private_key,
                    database_path=database_path
                )
            elif file_in and certificate_crt and private_pem and only_ssl:
                return network.Host.FTPSSL.Server(
                    host=host,
                    port=port,
                    file_in=file_in,
                    certificate=certificate_crt,
                    private_pem=private_pem
                )
            elif file_in and not certificate_crt and not private_pem \
                    and not public_pem:
                return network.Host.FTPB64.Server(
                    host=host,
                    port=port,
                    file_in=file_in
                )
            else:
                raise VPRuntimeError(
                    message="Missing or additional arguments for FTP "
                            "server operation.")
        elif mode == 'client':
            if file_out and certificate_crt and private_key and public_key:
                return network.Host.FTPVPPSSL.Client(
                    host=host,
                    port=port,
                    private_key=private_key,
                    public_key=public_key,
                    certificate=certificate_crt,
                    file_out=file_out
                )
            if file_out and not certificate_crt and private_key and public_key:
                return network.Host.FTPVPP.Client(
                    host=host,
                    port=port,
                    public_key=public_key,
                    private_key=private_key,
                    file_out=file_out
                )
            elif file_out and certificate_crt:
                return network.Host.FTPSSL.Client(
                    host=host,
                    port=port,
                    file_out=file_out,
                    certificate=certificate_crt
                )
            elif file_out and not certificate_crt:
                return network.Host.FTPB64.Client(
                    host=host,
                    port=port,
                    file_out=file_out
                )
            else:
                raise VPRuntimeError(
                    message="Missing or additional arguments for FTP "
                            "client operation.")
    elif operation == 'c2':
        if mode == 'server':
            if certificate_crt and private_key and not only_ssl:
                return network.Host.RevShellVPPSSL.Server(
                    host=host,
                    port=port,
                    private_key=private_key,
                    certificate=certificate_crt,
                    database_path=database_path,
                    private_pem=private_pem
                )
            elif not certificate_crt and private_key:
                return network.Host.RevShellVPP.Server(
                    host=host,
                    port=port,
                    private_key=private_key,
                    database_path=database_path
                )
            elif certificate_crt and private_pem and only_ssl:
                return network.Host.RevShellSSL.Server(
                    host=host,
                    port=port,
                    private_pem=private_pem,
                    certificate=certificate_crt
                )
            elif not certificate_crt and not private_pem and not public_pem:
                return network.Host.RevShellB64.Server(
                    host=host,
                    port=port
                )
            else:
                raise VPRuntimeError(
                    message="Missing or additional arguments for Reverse "
                            "Shell server operation.")
        elif mode == 'client':
            if public_key and private_key and certificate_crt:
                return network.Host.RevShellVPPSSL.Client(
                    host=host,
                    port=port,
                    public_key=public_key,
                    private_key=private_key,
                    certificate=certificate_crt
                )
            elif not certificate_crt and public_key and private_key:
                return network.Host.RevShellVPP.Client(
                    host=host,
                    port=port,
                    public_key=public_key,
                    private_key=private_key
                )
            elif certificate_crt and not private_key and not public_key:
                return network.Host.RevShellSSL.Client(
                    host=host,
                    port=port,
                    certificate=certificate_crt
                )
            elif not certificate_crt and not private_pem and not public_pem:
                return network.Host.RevShellB64.Client(
                    host=host,
                    port=port
                )
            else:
                raise VPRuntimeError(
                    message="Missing or additional arguments for "
                            "Reverse Shell client operation.")
