from Crypto.PublicKey import RSA

from runtime.Credentials import Credentials
import crypter.rsa.key.get_password
import network.Chatroom
import network.SecureChatroom
from network.Host import Host


class HostFactory:
    @staticmethod
    def work(mode: str,
             operation: str,
             host: str,
             port: int,
             banner: str,
             private_key: RSA.RsaKey = None,
             public_key: RSA.RsaKey = None,
             certificate_crt: str = None,
             database_path: str = None,
             target: str = None,
             ) -> Host:
        if not banner:
            banner = 'VP-Server'
        if operation == 'chat':
            if mode == 'server':
                if private_key:
                    return network.SecureChatroom.Server(
                        host=host,
                        port=port,
                        banner=banner,
                        private_key=private_key,
                        database_path=database_path)
                if not private_key:
                    return network.Chatroom.Server(
                        host=host,
                        port=port,
                        banner=banner)
            elif mode == 'client':
                if private_key and public_key:
                    return network.SecureChatroom.Client(
                        host=host,
                        port=port,
                        private_key=private_key,
                        public_key=public_key)
                else:
                    return network.Chatroom.Client(
                        host=host,
                        port=port)
