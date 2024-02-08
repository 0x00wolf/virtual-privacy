from crypter.rsa.key.get_password import get_password
from crypter.rsa.key.generate_keypair import generate_keypair


def interactive_keypair(private_key_path=None,
                        public_key_path=None):
    """
    Interactive function for generating a new RSA keypair with
    optional private key password encryption.

    Args:

    Returns:
        None (None): If successful saves keys to disk
    """

    welcome = input(
        "\n[*] GENERATING A NEW RSA KEYPAIR:\n"
        "\n[>] Hit enter to continue: ")
    encryption = input(
        "\n[*] Encrypt the RSA private key?"
        "\n[-] Input 'y' to encrypt the private key "
        "or hit 'enter' to continue.\n"
        "\n[>] Selection: ")
    if encryption == 'y':
        password = get_password()
    else:
        password = None
    if private_key_path and public_key_path:
        pass
    else:
        private_key_path = input(
            f"\n[*] Enter a custom path & filename for the RSA private key."
            f"\n[-] Important: Extension should be '.pem'."
            f"\n[-] Suggested path: "
            f"./keys/local/username_private.pem\n"
            f"\n[>] Selection: ")
        public_key_path = input(
            f"\n[*] Enter a custom path & filename for the RSA public key."
            f"\n[-] Important: Extension should be '.pem'."
            f"\n[-] Suggested path: "
            f"./keys/local/username_public.pem\n"
            f"\n[>] Selection: ")
    generate_keypair(private_key_file_out=private_key_path,
                     public_key_file_out=public_key_path,
                     password=password)
