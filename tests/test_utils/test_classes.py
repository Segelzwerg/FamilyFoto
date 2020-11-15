from family_foto.models.file import File


class UnsupportedFileType(File):
    @property
    def path(self):
        raise NotImplementedError

    @property
    def image_view(self):
        raise NotImplementedError

    @property
    def meta(self):
        raise NotImplementedError

    @property
    def height(self):
        raise NotImplementedError

    @property
    def width(self):
        raise NotImplementedError
