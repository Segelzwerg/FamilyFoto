from typing import List

import deprecation
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from family_foto.models import db, users_roles
from family_foto.models.auth_token import AuthToken
from family_foto.models.role import Role
from family_foto.models.user_settings import UserSettings


class User(UserMixin, db.Model):  # lgtm [py/missing-equals]
    """
    Database entity of an user.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(255), unique=True)
    active = db.Column(db.Boolean())

    roles = relationship('Role', secondary=users_roles, uselist=True)
    settings = relationship('UserSettings', foreign_keys='UserSettings.user_id',
                            back_populates='user', uselist=False, lazy='subquery')
    files = relationship('File', foreign_keys='File.user')
    token = relationship('AuthToken', foreign_keys='AuthToken.user_id', uselist=False)

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

    def add_role(self, role: Role) -> None:
        """
        Adds a role to an user.
        :param role: to add
        """
        self.roles.append(role)

    @deprecation.deprecated(deprecated_in='0.2', removed_in='1.0',
                            current_version=deprecation.__version__,
                            details='Use has_at_least_role_instead')
    def has_role(self, role_name: str) -> bool:
        """
        Checks if the user has this role.
        :param role_name: name of the role
        :return: boolean if the user has a given role
        """
        return any(role.name == role_name for role in self.roles)

    def has_at_least_role(self, role_level: int):
        """
        Checks if a user has at least role.
        :param role_level:
        :type role_level:
        :return:
        :rtype:
        """
        return any(role.level <= role_level for role in self.roles)

    def get_media(self):
        """
        Gets all media files from this user.
        :return: List of file objects.
        """
        user_photos = User.query.filter_by(id=self.id).first().files
        user_shared = UserSettings.query.filter(
            UserSettings.share_all.any(User.id == self.id)).all()
        for user in user_shared:
            user_photos.extend(User.query.filter_by(id=user.id).first().files)
        return user_photos

    def share_all_with(self, other_users: ('User', List['User'])) -> None:
        """
        Share all photos with users. It also revokes user privileges if not in list.
        :param other_users: the user/s all photos will be shared with
        :type other_users: Union of a single user or a list of users
        """
        if not self.settings:
            raise AttributeError(f'There are no user settings for the user with the id: {self.id}')
        if not isinstance(other_users, list):
            other_users = [other_users]
        for other_user in other_users:
            self.settings.share_all_photos_with(other_user)
        revoked_users = [user for user in self.settings.share_all if user not in other_users]
        for revoked_user in revoked_users:
            self.settings.revoke_sharing(revoked_user)

    def has_general_read_permission(self, other_user: 'User') -> bool:
        """
        Checks if the other use is allowed to view all photos.
        """
        return self.settings.has_all_sharing(other_user)

    def get_token(self) -> AuthToken:
        """
        Retrieves a new token or the current one.
        :return: an AuthToken
        """

        if self.token is None:
            self._create_token()
        elif not self.token.check(self.id):
            AuthToken.query.filter_by(id=self.token.id).delete()
            self._create_token()
        db.session.add(self.token)
        db.session.commit()
        return self.token

    def _create_token(self):
        auth_token = AuthToken.create_token(self)
        self.token = auth_token

    def approve(self):
        """
        Approve user by activating they.
        """
        self.active = True

    @staticmethod
    def all_user_asc():
        """
        Retrieves all users from the database and returns them in ascending order.
        """
        return sorted([[user.id, user.username] for user in User.query.all()],
                      key=lambda user: user[1])
