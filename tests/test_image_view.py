from tests.base_login_test_case import BaseLoginTestCase


class ImageViewTestCase(BaseLoginTestCase):
    """
    Tests the image route.
    """

    def test_route(self):
        self.client.get('/image/example.jpg')
