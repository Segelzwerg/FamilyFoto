from typing import List, Union

from flask_login import UserMixin
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from family_foto.models import db
from family_foto.models.user_settings import UserSettings


class User(UserMixin, db.Model):
    """
    Database entity of an user.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    settings = relationship('UserSettings', foreign_keys='UserSettings.user_id',
                            back_populates='user', uselist=False)
    photos = relationship('Photo')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password: str) -> None:
        """
        Sets the password of an user.
        :param password: The new plain text password.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        :param password: the plain text password typed in by the user
        :return: boolean if the hash code does match
        """
        return check_password_hash(self.password_hash, password)

    def get_photos(self):
        """
        Gets all photos from this user.
        :return: List of photo objects.
        """
        user_photos = User.query.filter_by(id=self.id).first().photos
        user_shared = UserSettings.query.filter(
            UserSettings.share_all.any(User.id == self.id)).all()
        for user in user_shared:
            user_photos.extend(User.query.filter_by(id=user.id).first().photos)
        return user_photos

    def share_all_with(self, other_users: Union['User', List['User']]) -> None:
        """
        Share all photos with users
        :param other_users: the user/s all photos will be shared with
        :type other_users: Union of a single user or a list of users
        """
        if not self.settings:
            raise AttributeError(f'There are no user settings for the user with the id: {self.id}')
        if not isinstance(other_users, list):
            other_users = [other_users]
        for other_user in other_users:
            self.settings.share_all_photos_with(other_user)

    @staticmethod
    def all_user_asc():
        """
        Retrieves all users from the database and returns them in ascending order.
        """
        return sorted([[user.id, user.username] for user in User.query.all()],
                      key=lambda user: user[1])
