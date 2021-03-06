from flask_login import current_user

from family_foto import add_user, Role
from family_foto.models import db
from family_foto.models.photo import Photo
from tests.base_login_test_case import BaseLoginTestCase


class UserLoggedInTestCase(BaseLoginTestCase):
    """
    Tests user behaviour for a logged in user.
    """

    def test_show_shared(self):
        """
        Tests if an user can see photos that others shared with him/her/it.
        """
        user_role = Role.query.filter_by(name='user').first()

        other_user = add_user('sharer', 'sharing', [user_role])
        other_photo = Photo(filename='other-photo.jpg', user=other_user.id)
        db.session.add(other_photo)
        db.session.commit()
        other_user.share_all_with(current_user)
        photos = current_user.get_media()
        self.assertIn(other_photo, photos)
