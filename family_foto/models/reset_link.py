from datetime import datetime, timedelta
from secrets import token_urlsafe

from family_foto.models import db


class ResetLink(db.Model):
    """
    Stores links which where sent to reset a password.
    """
    id = db.Column(db.Integer, primary_key=True, index=True, unique=True)
    link_hash = db.Column(db.String(32), index=True, unique=True)
    active = db.Column(db.Boolean, default=False)
    expiration = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    user = db.relationship('User', foreign_keys=[user_id], uselist=False)

    def set_active(self):
        """
        Sets the link active. Now user are allowed to change their password.
        """
        self.active = True

    def is_active(self):
        """
        If true user change their password.
        """
        return self.active

    @staticmethod
    def generate_link(user, expires_in: int = 3600) -> 'ResetLink':
        """
        Generates a hash for the password reset url.
        :param user: the object of the user how requested a reset
        :param expires_in: the time until the link expires. Default 6h.
        """
        now = datetime.utcnow()
        link_hash = token_urlsafe(32)
        expiration = now + timedelta(seconds=expires_in)
        link = ResetLink(user=user, link_hash=link_hash, expiration=expiration)
        db.session.add(link)
        return link
