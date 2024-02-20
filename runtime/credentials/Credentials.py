from dataclasses import dataclass
from Crypto.PublicKey import RSA


class Credentials:
    """
    Credentials are returned by the ConfigurationM
    """
    def __init__(self,
                 private_key: RSA.RsaKey = None,
                 public_key: RSA.RsaKey = None,
                 certificate_crt: str = None):
        self.private_key = private_key
        self.public_key = public_key
        self.certificate_crt = certificate_crt
