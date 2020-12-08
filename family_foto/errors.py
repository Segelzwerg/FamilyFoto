class UploadError(IOError):
    """
    Exception raised if something happens during upload.
    """

    def __init__(self, filename: str, message):
        self.filename = filename
        self.message = message
        super().__init__(self.message)
