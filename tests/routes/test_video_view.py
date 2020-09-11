from flask_api import status

from family_foto.models import db
from tests.base_video_test_case import BaseVideoTestCase


class VideoViewTestCase(BaseVideoTestCase):
    """
    Tests the route of /video/<file>
    """

    def test_video_view(self):
        """
        Tests the preview of the video.
        """
        db.session.add(self.video)
        db.session.commit()
        response = self.client.get('/video/example.mp4')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
