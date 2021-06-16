from flask_api import status
from flask_login import current_user

from family_foto.models.file import File
from tests.base_login_test_case import BaseLoginTestCase
from tests.base_test_case import BaseTestCase
from tests.test_utils.assertions import assertImageIsLoaded
from tests.test_utils.mocking import mock_user
from tests.test_utils.tasks import upload_test_file


class ProtectedGalleryTestCase(BaseLoginTestCase):
    """
    Tests the protected gallery under /public
    """

    def test_route(self):
        """
        Tests if a user can view it.
        """
        response = self.client.get('/public')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_unauthorized_access(self):
        """
        Tests if a anonymous user will be redirected.
        """
        self.patcher.stop()
        response = self.client.get('/public')
        self.assertEqual(status.HTTP_302_FOUND, response.status_code)

    def test_images_is_shared(self):
        """
        Tests if an image is shared in the public gallery.
        """
        filename = 'test.jpg'
        upload_test_file(self.client, filename)
        file = File.query.filter_by(filename=filename).first()
        file.protected = True
        response = self.client.get('/public')
        assertImageIsLoaded(self, response)


class GuestUserProtectedGalleryTestCase(BaseTestCase):
    """
    Tests protected gallery with a guest user.
    """

    def setUp(self):
        super().setUp()
        mock_user(self, 'marcel', 'guest')

    def test_route_with_approval(self):
        """
        Tests if a user can view it.
        """
        # https://github.com/PyCQA/pylint/issues/3793
        # pylint: disable=E0237
        current_user.active = True
        response = self.client.get('/public')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_route_without_approval(self):
        """
        Tests if a user can't view it.
        """
        response = self.client.get('/public')
        self.assertEqual(status.HTTP_302_FOUND, response.status_code)

    def tearDown(self):
        self.patcher.stop()
        super().tearDown()
