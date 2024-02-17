import subprocess

from crypter.CrypterError import CrypterError


def self_sign(private_key_path, certificate_export_path):
    print(f"[*] Path to RSA private key: {private_key_path}")
    print(f"[*] Self-signing certificate"
          f"\n[ ] Export path: {certificate_export_path}")
    try:
        subprocess.run([
            "openssl",
            "req",
            "-new",
            "-x509",
            "-key",
            private_key_path,
            "-out",
            certificate_export_path,
            "-days",
            "365"])
    except subprocess.CalledProcessError as e:
        raise CrypterError(f"Self-signing error {e}")
    try:
        with open(certificate_export_path, 'r') as f:
            data = f.read()
        if data:
            print("[*] Process successful")
    except FileNotFoundError as e:
        raise CrypterError(message=f"{e}")
