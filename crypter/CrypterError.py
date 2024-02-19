class CrypterError(Exception):
    """
    A class to handle execution flow after an error arises.

    Args:
        message (str): Information about the specific error, and the
        error code.
        continue_execution (bool): Boolean to indicate whether or not the
        error is fatal.
    """

    def __init__(self, message: str = None):
        super().__init__(message)
        self.message = message
