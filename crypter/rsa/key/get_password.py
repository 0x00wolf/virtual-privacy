from getpass import getpass


def get_password():
    """
    Get user to input & verify the password for their RSA private key
    without printing the password to the terminal.

    Returns:
          password (str): User's RSA private key password
    """

    while True:
        password = getpass("\n[*] Input the password for your RSA private key."
                           "\n[>] password: ")
        verify = getpass("\n[*] Confirm password."
                         "\n[>] password: ")
        if password == verify:
            break
        else:
            print("\n[!] Error passwords do not match!"
                  "\n[*] Try again.")
    return password
