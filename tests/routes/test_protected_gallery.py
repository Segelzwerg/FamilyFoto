from flask_api import status

from family_foto import File
from tests.base_login_test_case import BaseLoginTestCase
from tests.test_utils.assertions import assertImageIsLoaded
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
