from pytest import raises

from family_foto.models.file import File
from tests.base_test_case import BaseTestCase


class FileTestCase(BaseTestCase):
    """
    Tests the base file class.
    """

    def setUp(self):
        super().setUp()
        self.file = File(filename='test.txt')

    def test_path(self):
        """
        Test path is not implemented.
        """
        with raises(NotImplementedError):
            _ = self.file.path

    def test_meta(self):
        """
        Test meta is not implemented.
        """
        with raises(NotImplementedError):
            _ = self.file.meta

    def test_thumbnail(self):
        """
        Test thumbnail is not implemented.
        """
        with raises(NotImplementedError):
            _ = self.file.thumbnail(200, 200)
