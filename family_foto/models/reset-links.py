from secrets import token_urlsafe

from family_foto.models import db


class ResetLink(db.Model):
    """
    Stores links which where sent to reset a password.
    """
    id = db.Column(db.Integer, primary_key=True, index=True, unique=True)
    link_hash = db.Column(db.String(32), index=True, unique=True)
    expiration = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    user = db.relationship('User', foreign_keys=[user_id], uselist=False)

    def generate_link(self) -> None:
        """
        Generates a hash for the password reset url.
        """
        self.link_hash = token_urlsafe(32)
