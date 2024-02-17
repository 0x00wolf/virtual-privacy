import subprocess


def quick_gen_privatekey_cert(private_key, certificate):
    try:
        subprocess.run(args=[
            "openssl",
            "req",
            "-newkey",
            "rsa:3072",
            "-nodes",
            "-keyout",
            private_key,
            "-x509",
            "-days",
            "365",
            "out",
            certificate],
            check=True)
        print(f"[*] Generating RSA private key & self-signed certificate "
              f"successful:\n"
              f"[ ] Exporting RSA private key to: {private_key}\n"
              f"[ ] Exporting signed certificate to: {certificate}")
    except subprocess.CalledProcessError as e:
        raise CrypterError(f"Fast key gen and self-signed certificate "
                           f"error {e}.")
