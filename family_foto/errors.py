class UploadError(IOError):
    """
    Exception raised if something happens during upload.
    """

    def __init__(self, filename: str, message):
        self.filename = filename
        self.message = message
        super().__init__(self.message)


class InActiveWarning(Warning):
    """
    Warning raised if an inactive user tries to access content.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class PasswordError(Exception):
    """
    Exception raised if some was wrong with the password.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(message)
