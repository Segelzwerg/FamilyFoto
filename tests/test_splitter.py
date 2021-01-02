from family_foto.front_end_wrapper.month import Month
from family_foto.front_end_wrapper.utils.splitter import Splitter
from family_foto.front_end_wrapper.year import Year
from tests.base_media_test_case import BaseMediaTestCase


class SplitterTestCase(BaseMediaTestCase):
    """
    Tests the file splitter.
    """

    def test_one_photo(self):
        """
        Tests splitting with one photo.
        """
        splitter = Splitter([self.photo])
        year = 2020
        august = Month([self.photo], 8, year)
        expected_year = Year([august], year)
        self.assertEqual(splitter.split(), {year: expected_year})

    def test_one_video(self):
        """
        Tests splitting with one video.
        """
        splitter = Splitter([self.video])
        year = 2015
        august = Month([self.video], 8, year)
        expected_year = Year([august], year)
        self.assertEqual(splitter.split(), {year: expected_year})

    def test_both(self):
        """
        Test with both files from above.
        """
        splitter = Splitter([self.video, self.photo])
        august_fifteen = Month([self.video], 8, 2015)
        august_twenty = Month([self.photo], 8, 2020)
        splits = splitter.split()
        self.assertDictEqual(splits, {2020: Year([august_twenty], 2020),
                                      2015: Year([august_fifteen], 2015)})
