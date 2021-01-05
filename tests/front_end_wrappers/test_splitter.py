import os

from family_foto.front_end_wrapper.month import Month
from family_foto.front_end_wrapper.utils.splitter import Splitter
from family_foto.front_end_wrapper.year import Year
from family_foto.models import db
from family_foto.models.photo import Photo
from tests.base_login_test_case import BaseLoginTestCase
from tests.base_media_test_case import BaseMediaTestCase


class SplitterTestCase(BaseLoginTestCase, BaseMediaTestCase):
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

    def test_existing_year(self):
        """
        Tests if two files are created in the same year.
        """
        db.session.close()
        with self.client:
            filename = 'example.jpg'
            photo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', filename)
            photo = open(photo_path, 'rb')
            data = dict(file=[(photo, filename)])
            self.client.post('/upload',
                             content_type='multipart/form-data',
                             data=data)
            photo.close()
            other_photo = Photo.query.filter_by(filename=filename).first()
            splitter = Splitter([self.photo, other_photo])
            splits = splitter.split()
            august = Month([self.photo, other_photo], 8, 2020)
            self.assertDictEqual(splits, {2020: Year([august], 2020)})
