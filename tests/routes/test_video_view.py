from flask_api import status

from family_foto import add_user
from family_foto.models import db
from family_foto.models.role import Role
from family_foto.models.video import Video
from tests.base_login_test_case import BaseLoginTestCase
from tests.base_video_test_case import BaseVideoTestCase


class VideoViewTestCase(BaseLoginTestCase, BaseVideoTestCase):
    """
    Tests the route of /videos/<hash_group>/<file_hash>/<filename>
    """

    def setUp(self):
        super().setUp()
        self.video.user = self.mock_current_user.id
        self.user_role = Role.query.filter_by(name='user').first()
        db.session.add(self.video)
        db.session.commit()

    def test_video_view(self):
        """
        Tests the preview of the video.
        """
        response = self.client.get(self.video.url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_url(self):
        """
        Tests the direct view of the video file.
        """
        with self.client:
            response = self.client.get(self.video.url)
            self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_authorized_access(self):
        """
        Tests if unauthorized access is denied.
        """
        owner = add_user('owner', '123', [self.user_role])
        video = Video(filename='other_file.mp4', hash='zzzz', user=owner.id)
        db.session.add(video)
        db.session.commit()
        response = self.client.get(video.url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
