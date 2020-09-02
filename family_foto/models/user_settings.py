from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from family_foto.logger import log
from family_foto.models import db


class UserSettings(db.Model):
    """
    Entity of the user settings
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), unique=True, nullable=False)
    share_all_id = db.Column(db.Integer, ForeignKey('user.id'))

    user = relationship('User', foreign_keys=[user_id], back_populates='settings', uselist=False)
    share_all = relationship('User', foreign_keys=[share_all_id], uselist=True)

    def __repr__(self):
        return f'<UserSettings of {self.user}>'

    def share_all_photos_with(self, other_user):
        """
        Allows the user to see the user's photos.
        :param other_user: user how will get access to the photos
        """
        if other_user is None:
            raise AttributeError('other_user must not be None.')
        self.share_all.append(other_user)
        log.info(f'{self.user} shares photos with {other_user}.')

    def revoke_sharing(self, other_user):
        """
        Revokes the privileges of the other use.
        :param other_user: the user how rights will get revoked
        """
        if other_user is None:
            raise AttributeError('other_user must not be None')
        self.share_all.remove(other_user)
        log.info(f'{self.user} revokes sharing of photos with {other_user}.')
