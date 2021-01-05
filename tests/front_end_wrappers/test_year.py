from family_foto.front_end_wrapper.month import Month
from family_foto.front_end_wrapper.year import Year
from tests.base_photo_test_case import BasePhotoTestCase


class YearTestCase(BasePhotoTestCase):
    """
    Test the year wrapper.
    """

    def test_not_equal(self):
        """
        Tests if year is not a month.
        """
        month = Month([self.photo], 8, 2020)
        year = Year([month], 2020)
        self.assertFalse(year == month)
