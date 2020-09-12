from flask_api import status

from family_foto.models import db
from tests.base_login_test_case import BaseLoginTestCase
from tests.base_video_test_case import BaseVideoTestCase


class VideoViewTestCase(BaseLoginTestCase, BaseVideoTestCase):
    """
    Tests the route of /video/<file>
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
        response = self.client.get('/image/example.mp4')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_url(self):
        """
        Tests the direct view of the video file.
        """
        with self.client:
            response = self.client.get('/videos/example.mp4')
            self.assertEqual(status.HTTP_200_OK, response.status_code)
