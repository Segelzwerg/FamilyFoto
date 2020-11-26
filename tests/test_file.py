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

    def test_image_view(self):
        """
        Test image view is not implemented.
        """
        with raises(NotImplementedError):
            _ = self.file.image_view

    def test_meta(self):
        """
        Test meta is not implemented.
        """
        with raises(NotImplementedError):
            _ = self.file.meta

    def test_height(self):
        """
        Test height is not implemented.
        """
        with raises(NotImplementedError):
            _ = self.file.height

    def test_width(self):
        """
        Test width is not implemented.
        """
        with raises(NotImplementedError):
            _ = self.file.width
