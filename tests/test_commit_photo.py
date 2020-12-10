from family_foto.models import db
from family_foto.models.photo import Photo
from tests.base_photo_test_case import BasePhotoTestCase


class CommitPhotoTestCase(BasePhotoTestCase):
    """
    Tests committing a photo.
    """

    def test_commit(self):
        """Tests committing the file works"""
        db.session.add(self.photo)
        db.session.commit()

        photo = Photo.query.get(self.photo.id)
        self.assertEqual(self.photo, photo)
