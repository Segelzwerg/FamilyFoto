from flask_api import status

from family_foto.models import db
from tests.base_login_test_case import BaseLoginTestCase
from tests.base_video_test_case import BaseVideoTestCase


class VideoViewTestCase(BaseLoginTestCase, BaseVideoTestCase):
    """
    Tests the route of /videos/<hash_group>/<file_hash>/<filename>
    """

    def setUp(self):
        super().setUp()
        self.video.user = self.mock_current_user.id

    def test_video_view(self):
        """
        Tests the preview of the video.
        """
        db.session.add(self.video)
        db.session.commit()
        response = self.client.get(self.video.url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_url(self):
        """
        Tests the direct view of the video file.
        """
        with self.client:
            response = self.client.get(self.video.url)
            self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_non_existing_file(self):
        """
        Test if exception is thrown if file does not exists.
        :return:
        :rtype:
        """
        with self.client:
            with self.assertRaises(FileExistsError):
                self.client.get('/videos/cd/cdef/non.mp4')
