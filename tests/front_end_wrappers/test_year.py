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

    def test_add_file_to_empty_year(self):
        """
        Tests if you can add a file to an empty year.
        """
        year = Year([], 2020)
        year.add_file(self.photo)
        expected_year = Year([Month([self.photo], self.photo.month, self.photo.year)],
                             self.photo.year)
        self.assertEqual(year, expected_year)
