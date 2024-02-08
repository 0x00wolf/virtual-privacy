class DatabaseError(Exception):
    """
    A class to encapsulate low level error handling.

    Args:
        message (str): Information about the specific error, and the
        error code.
        continue_execution (bool): Boolean to indicate whether or not the
        error is fatal.
    """

    def __init__(self, message: str = None):
        super().__init__(message)
        self.message = message
