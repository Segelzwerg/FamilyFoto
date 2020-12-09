from tests.base_login_test_case import BaseLoginTestCase


class VideoRouteTestCase(BaseLoginTestCase):
    """
    Tests route directly accessing media.
    """

    def test_non_existing_file(self):
        """
        Test if exception is thrown if file does not exists.
        :return:
        :rtype:
        """
        with self.client:
            with self.assertRaises(FileExistsError):
                self.client.get('/videos/cd/cdef/non.mp4')
