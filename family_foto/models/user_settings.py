from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from family_foto.models import db


class UserSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), unique=True, nullable=False)
    share_all_id = db.Column(db.Integer, ForeignKey('user.id'))

    user = relationship('User', foreign_keys=[user_id], back_populates='settings', uselist=False)
    share_all = relationship('User', foreign_keys=[share_all_id], uselist=True)

    def share_all_photos_with(self, other_user):
        """
        Allows the user to see the user's photos.
        :param other_user: id of the other user
        :type other_user: User
        """
        self.share_all.append(other_user)
        db.session.add(self)
