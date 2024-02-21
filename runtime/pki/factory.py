from runtime.VPRuntimeError import VPRuntimeError
from crypter.CrypterError import CrypterError
import crypter.rsa.key
import crypter.pki


def factory(args):
    if args.generate_pki == 'rsa':
        crypter.rsa.key.interactive_keypair(
            private_key_path=args.private_key,
            public_key_path=args.public_key)
    if args.generate_pki == 'self-sign':
        if not args.private_key:
            raise VPRuntimeError(message=f"Missing required arguments for X509 "
                                         f"self-signing.\n[ ] Operation "
                                         f"requires: --private-key & "
                                         f"--certificate")
        if not args.certificate:
            args.certificate = './cert.crt'
        print(f"[*] Exporting self-signed certificate to: "
              f"{args.certificate}")
        crypter.pki.self_sign(
            private_key_path=args.private_key,
            certificate_export_path=args.certificate)
    elif args.generate_pki == 'fast-gen':
        if not args.private_key:
            args.private_key = 'privkey.pem'
        if not args.certificate:
            args.certificate = 'cert.crt'
        crypter.pki.gen_cert_key(
            private_key=args.private_key,
            certificate=args.certificate)
    elif args.generate_pki == 'root-ca':
        crypter.pki.easy_infrastructure()
