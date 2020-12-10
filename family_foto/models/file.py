import os
from abc import abstractmethod
from datetime import datetime
from typing import List, Union

from flask import current_app
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from family_foto.models import db
from family_foto.models.user import User


class File(db.Model):
    # pylint: disable=too-few-public-methods
    """
    Database entity of a file.
    """
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(64))
    file_type = db.Column(db.String(64))
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.Column(db.Integer, ForeignKey('user.id'))
    share_with_id = db.Column(db.Integer, ForeignKey('user.id'))
    protected = db.Column(db.Boolean, default=False)
    hash = db.Column(db.String(128), index=True, unique=True)
    shared_with = relationship('User', foreign_keys=[share_with_id], uselist=True)

    __mapper_args__ = {
        'polymorphic_identity': 'file',
        'polymorphic_on': file_type
    }

    @property
    def get_hash(self):
        """
        Returns the hash as string.
        """
        return str(self.hash)

    @property
    @abstractmethod
    def path(self):
        """
        Path of the file on the server.
        """
        raise NotImplementedError('Each file type has its directory.')

    @property
    def abs_path(self):
        """
        Returns absolute path of the photo.
        """
        return os.path.abspath(os.path.join(current_app.instance_path, self.path))

    @property
    def url(self):
        """
        Returns url of the file.
        """
        return f'/{self.path}'

    @property
    def image_view(self):
        """
        Returns the url to image view.
        """
        return f'/image/{self.hash}'

    @property
    @abstractmethod
    def meta(self):
        """
        Meta data of the file.
        """
        raise NotImplementedError('Each media type has is custom meta data retriever.')

    @property
    @abstractmethod
    def height(self):
        """
        Returns the image height.
        """
        raise NotImplementedError('Each media type has is custom meta data retriever.')

    @property
    @abstractmethod
    def width(self):
        """
        Returns image width
        """
        raise NotImplementedError('Each media type has is custom meta data retriever.')

    def share_with(self, other_users: Union[User, List[User]]) -> None:
        """
        Share this photo with an user.
        :param other_users: the other user the photo will be shared with.
        """
        if not isinstance(other_users, list):
            other_users = [other_users]
        for user in other_users:
            self.shared_with.append(user)

    def has_read_permission(self, other_user: User) -> bool:
        """
        Checks if the other user has permission to view that photo.
        """
        if self.user == other_user.id:
            return True
        if other_user in self.shared_with:
            return True
        user = User.query.get(self.user)
        return user.has_general_read_permission(other_user)

    @staticmethod
    def _replace_empty(value: bytes):
        """
        Tries to replace '\x00'
        """
        return str(value).replace('\x00', '')
