from werkzeug.datastructures import FileStorage

from family_foto.models.file import File


def compare_files(exists: File, file: FileStorage):
    """
    Compares two files by content.
    :param exists: this file is already on the server
    :param file: this is the uploaded file
    :return: True if equal, False otherwise
    """
    existing_file = open(exists.abs_path, 'rb')
    uploaded_read = file.stream.read()
    existing_read = existing_file.read()
    return uploaded_read == existing_read
