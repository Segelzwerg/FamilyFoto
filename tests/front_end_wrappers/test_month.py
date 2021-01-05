from family_foto.front_end_wrapper.month import Month
from family_foto.front_end_wrapper.year import Year
from tests.base_photo_test_case import BasePhotoTestCase


class MonthTestCase(BasePhotoTestCase):
    """
    Tests the file wrapper for months.
    """

    def setUp(self):
        super().setUp()
        self.month = Month([self.photo], 8, 2020)

    def test_not_equal(self):
        """
        Tests if year is not a month.
        """
        month = self.month
        year = Year([month], 2020)
        self.assertFalse(month == year)

    def test_thumbnails(self):
        """
        Tests if the thumbnails are correctly returned.
        """
        expected_path = f'/photos/{self.photo.hash[:2]}/{self.photo.hash}/200_200_example.jpg'
        self.assertEqual(self.month.get_thumbnails(200, 200), [expected_path])
