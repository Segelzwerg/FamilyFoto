import os
from unittest.mock import Mock, patch

import ffmpeg
import pytest

from family_foto.services.thumbnail_service import generate, generate_all
from tests.base_media_test_case import BaseMediaTestCase
from tests.test_utils.test_classes import UnsupportedFileType


class TestThumbnailService(BaseMediaTestCase):
    """
    Tests the thumbnail service.
    """

    def test_generate_from_photo(self):
        """
        Tests the thumbnail service for a photo.
        """
        path = generate(self.photo)
        self.assertEqual(f'/{os.path.dirname(self.photo.path)}/400_400_example.jpg', path)

    def test_generate_from_video(self):
        """
        Tests the thumbnail service for a video.
        """
        path = generate(self.video)
        self.assertEqual(f'/{os.path.dirname(self.video.path)}/400_400_example.mp4.jpg', path)

    def test_generate_unsupported_type(self):
        """
        Tests if an error is raised for an unsupported type.
        """
        with self.assertRaises(TypeError):
            generate(UnsupportedFileType())

    def test_video_thumbnail_already_exists(self):
        """
        Tests if the thumbnail is no recreated.
        """
        _ = generate(self.video)
        with patch('family_foto.utils.image.resize') as resize:
            _ = generate(self.video)
            resize.assert_not_called()

    def test_photo_thumbnail_already_exists(self):
        """
        Tests if the thumbnail is no recreated.
        """
        _ = generate(self.photo)
        with patch('resizeimage.resizeimage.resize_width') as resize:
            _ = generate(self.photo)
            resize.assert_not_called()

    @patch('family_foto.services.thumbnail_service._resized_frame',
           Mock(side_effect=ffmpeg.Error(cmd='input', stdout=True, stderr=True)))
    def test_thumbnail_fail(self):
        """
        Tests a failure in creating a thumbnail raises an error.
        """
        with self.assertRaisesRegex(IOError, 'Could not read frames from'):
            _ = generate(self.video)

    @pytest.mark.asyncio
    async def test_async_task(self):
        """
        Test the basic thumbnail service functionality.
        """
        files = [self.photo.id]
        await generate_all(files, 200, 200)
        path = f'/{os.path.dirname(self.photo.path)}/400_400_example.jpg'
        self.assertTrue(os.path.exists(path))
