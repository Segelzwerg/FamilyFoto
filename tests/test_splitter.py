from family_foto.front_end_wrapper.month import Month
from family_foto.front_end_wrapper.utils.splitter import Splitter
from family_foto.front_end_wrapper.year import Year
from tests.base_photo_test_case import BasePhotoTestCase


class SplitterTestCase(BasePhotoTestCase):
    """
    Tests the file splitter.
    """

    def test_one_photo(self):
        splitter = Splitter([self.photo])
        august = Month([self.photo], 8, 2020)
        expected_year = Year([august], 2020)
        self.assertEqual(splitter.split(), {2020: expected_year})
