import subprocess
import readline
import crypter
import sys


def easy_infrastructure():
    print("\n[*] GENERATING PUBLIC KEY INFRASTRUCTURE (PKI)")
    root_ca_pem = root_ca_private_key()
    root_ca_crt = root_ca_certificate(
        root_ca_pem=root_ca_pem)
    server_pem, server_public_pem = server_keypair()
    server_csr = create_csr(server_pem=server_pem)
    verify_csr(server_csr=server_csr)
    server_crt = sign_csr(root_ca_pem=root_ca_pem,
                          root_ca_crt=root_ca_crt,
                          server_csr=server_csr)
    verify_crt(server_crt)
    sys.exit()


def root_ca_private_key(root_ca_pem=None):
    input(
        "\n[*] GENERATING the root CERTIFICATE AUTHORITY (CA) RSA "
        "PRIVATE KEY:\n"
        "\n[>] Press enter to continue: ")
    if root_ca_pem:
        pass
    else:
        root_ca_pem = input(f"\n[*] Input the path and filename for storing "
                            f"the root CA RSA private key & insert a strong "
                            f"password when prompted."
                            f"\n[-] Suggested path: ./keys/local/rootCA.pem"
                            f"\n[!] Important: Extension must be '.pem'.\n"
                            f"\n[>] Selection: ")
    try:
        subprocess.run([
            "openssl",
            "genrsa",
            "-des3",
            "-out",
            root_ca_pem,
            "4096"],
            check=True)
    except subprocess.CalledProcessError:
        print("\n[!] Error generating root CA RSA private key."
              "\n[*] Exiting...")
        sys.exit()
    input(f"\n[*] SAVING root CA RSA PRIVATE KEY: {root_ca_pem}\n"
          f"\n[-] Press enter to continue: ")
    return root_ca_pem


def root_ca_certificate(root_ca_pem, root_ca_crt=None):
    input("\n[*] GENERATING the root CA CERTIFICATE:"
          "\n[-] Copies of the root CA are bundled with invite codes."
          "\n[-] PKI provides SSL encryption on top of VPC's "
          "encryption protocol."
          "\n[!] When prompted, enter the password for the VPC root "
          "CA RSA private key.\n"
          "\n[>] Press enter to continue: ")
    if root_ca_crt:
        pass
    else:
        root_ca_crt = input(f"\n[*] Input a path and filename for the root CA "
                            f"certificate."
                            f"\n[-] The certificate must be shared with every "
                            f"client who will connect to your server."
                            f"\n[!] Important: Extension must be '.crt'."
                            f"\n[-] Suggested path: './keys/local/rootCA.crt'\n"
                            f"\n[>] Selection: ")
        input("\n[>] Press enter for password prompt: ")
    try:
        subprocess.run([
            "openssl",
            "req",
            "-x509",
            "-new",
            "-nodes",
            "-key",
            root_ca_pem,
            "-sha256",
            "-days",
            "1024",
            "-out",
            root_ca_crt],
            check=True)
    except subprocess.CalledProcessError:
        print("\n[!] Error generating root CA certificate."
              "\n[*] Exiting...")
        sys.exit()
    input(f"\n[*] SAVING root CA CERTIFICATE as: {root_ca_crt}\n"
          f"\n[*] Press enter to continue:")
    return root_ca_crt


def server_keypair(server_pem=None, server_public_pem=None):
    input("\n[*] GENERATING an RSA KEY PAIR for the server\n"
          "\n[*] Press enter to continue ")
    if server_pem and server_public_pem:
        pass
    else:
        server_pem = input(f"\n[*] Enter a custom filename & path for the VPC "
                           f"server's RSA private key."
                           f"\n[!] Important: extension must be '.pem'."
                           f"\n[-] Suggested path: "
                           f"'./keys/local/server-private.pem'\n"
                           f"\n[>] Selection: ")
        server_public_pem = input(
            f"\n[*] Enter a custom filename & path for the VPC server's "
            f"RSA public key."
            f"\n[!] Important: Extension should be '.pem'."
            f"\n[-] Suggested path: './keys/local/server-public.pem'\n"
            f"\n[>] Selection: ")
    password = input("\n[*] Password protected keypair?"
                     "\n[-] 'y' or 'enter' to continue.\n"
                     "\n[>] Selection: ")
    if password == 'y':
        try:
            subprocess.run([
                "openssl",
                "genrsa",
                "-des3",
                "-out",
                server_pem,
                "3072"],
                check=True)
        except subprocess.CalledProcessError:
            print("\n[!] Error generating server keypair.\n[*] Exiting...")
            sys.exit()
    else:
        try:
            subprocess.run([
                "openssl",
                "genrsa",
                "-out",
                server_pem,
                "3072"],
                stderr=subprocess.DEVNULL,
                check=True)
        except subprocess.CalledProcessError:
            print("\n[!] Error generating server keypair.\n[*] Exiting...")
            sys.exit()
    if password:
        print("\n[*] Server's RSA private key generated. Re-enter the password"
              "to export the RSA public key to disk:")
        passwrd = crypter.rsa.key.get_password()
        private_key = crypter.rsa.key.load_key(pem_path=server_pem,
                                               password=passwrd)
    else:
        private_key = crypter.rsa.key.load_key(pem_path=server_pem)
    crypter.rsa.key.export_public_key(private_key=private_key,
                                      export_path=server_public_pem)
    input(f"\n[*] SAVING VPC server RSA PRIVATE KEY to: {server_pem}"
          f"\n[*] SAVING VPC server RSA PUBLIC KEY to: {server_public_pem}\n"
          f"\n[>] Press enter to continue: ")
    return server_pem, server_public_pem


def create_csr(server_pem, server_csr=None):
    input("\n[*] CREATING a CERTIFICATE SIGNING REQUEST (CSR) for the "
          "server:"
          "\n[-] The certificate signing request is where you specify "
          "the details for the certificate you want to generate for the "
          "VP Server."
          "\n[-] This request will be processed by the owner of the Root "
          "key (you in this case, since you created it earlier) to "
          "generate the certificate."
          "\n[!] IMPORTANT: You must specify the `Common Name` by "
          "\nproviding the IP address or domain name for the VPC server. "
          "Otherwise the certificate cannot be verified. "
          "If you are generating a localhost, use 'localhost' or "
          "'127.0.0.1'.\n"
          "\n[>] Press enter to continue: ")
    if server_csr:
        pass
    else:
        server_csr = input(f"\n[*] Enter a custom filename & path for the VPC "
                           f"server's certificate signing request (CSR)."
                           f"\n[!] Important: The extension must be '.csr'."
                           f"\n[-] Suggested path: "
                           f"'./keys/local/server-signing-request.csr'\n"
                           f"\n[>] Selection: ")
    try:
        subprocess.run([
            "openssl",
            "req",
            "-new",
            "-key",
            server_pem,
            "-out",
            server_csr],
            check=True)
    except subprocess.CalledProcessError:
        print("\n[!] Error generating server certificate signing "
              "request.\n[*] Exiting...")
    input(f"\n[*] SAVING server CSR as {server_csr}\n"
          f"\n[>] Press enter to continue: ")
    return server_csr


def verify_csr(server_csr):
    input("\n[*] VERIFY the CSR is accurate\n"
          "\n[>] Press enter to continue:")
    try:
        subprocess.run([
            "openssl",
            "req",
            "-in",
            server_csr,
            "-noout",
            "-text"],
            stderr=subprocess.DEVNULL,
            check=True)
    except subprocess.CalledProcessError:
        print("\n[!] Error verifying server certificate signing request."
              "\n[*] Exiting...")
        sys.exit()
    input("\n[*] Press enter to continue: ")


def sign_csr(root_ca_pem, root_ca_crt, server_csr, server_crt=None):
    print("\n[*] SIGN the server's CSR WITH the root CA RSA PRIVATE KEY:")
    if server_crt:
        pass
    else:
        server_crt = input(f"\n[*] Enter a filename & path for the VP "
                           f"server's signed certificate (CRT)."
                           f"\n[!] Important: File extension must be '.crt'."
                           f"\n[-] Suggested path: "
                           f"'./keys/local/server.crt'\n"
                           f"\n[>] Selection: ")
    input("\n[-] Enter the password for the root CA RSA private key when "
          "prompted.\n"
          "\n[>] Press enter to prompt for password:")
    try:
        subprocess.run([
            "openssl",
            "x509",
            "-req",
            "-in",
            server_csr,
            "-CA", root_ca_crt,
            "-CAkey",
            root_ca_pem,
            "-CAcreateserial",
            "-out",
            server_crt,
            "-days",
            "500",
            "-sha256"],
            stderr=subprocess.DEVNULL,
            check=True)
    except subprocess.CalledProcessError:
        print("\n[!] Error signing server certificate signing request."
              "\n[*] Exiting...")
        sys.exit()
    input(f"\n[*] SAVING CSR to {server_crt}\n"
          f"\n[>] Press enter to continue: ")
    return server_crt


def verify_crt(server_crt):
    input("\n[*] Press enter to VERIFY the SIGNED CERTIFICATE's contents: ")
    try:
        subprocess.run([
            "openssl",
            "x509",
            "-in",
            server_crt,
            "-text",
            "-noout"])
    except subprocess.CalledProcessError:
        print("\n[!] Error verifying root CA certificate."
              "\n[*] Exiting...")
        sys.exit()
    print("\n[*] PKI ESTABLISHED. Server is ready to rumble...")


if __name__ == '__main__':
    try:
        manual_mode()
    except KeyboardInterrupt:
        print('exiting...')