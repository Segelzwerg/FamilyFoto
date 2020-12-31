class FamilyFotoServerError(Exception):
    """
    Base exception for this server.
    """

    def __init__(self, message):
        self._message = message
        super().__init__(message)

    @property
    def message(self):
        """
        :returns: the message of the error
        """
        return self._message


class UploadError(FamilyFotoServerError):
    """
    Exception raised if something happens during upload.
    """

    def __init__(self, filename: str, message):
        self.filename = filename
        super().__init__(message)


class InActiveWarning(Warning):
    """
    Warning raised if an inactive user tries to access content.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class PasswordError(FamilyFotoServerError):
    """
    Exception raised if some was wrong with the password.
    """

    def __init__(self, message):
        super().__init__(message)
