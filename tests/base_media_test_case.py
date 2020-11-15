from tests.base_photo_test_case import BasePhotoTestCase
from tests.base_video_test_case import BaseVideoTestCase


class BaseMediaTestCase(BasePhotoTestCase, BaseVideoTestCase):
    """
    Collects all test cases for the every media types.
    """
