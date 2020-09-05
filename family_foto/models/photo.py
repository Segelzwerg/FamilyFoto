from datetime import datetime

from sqlalchemy import ForeignKey

from family_foto.models import db
from family_foto.models.user import User


class Photo(db.Model):
    # pylint: disable=too-few-public-methods
    """
    Database entity of a photo.
    """
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(64), index=True, unique=True)
    url = db.Column(db.String(128), unique=True)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.Column(db.Integer, ForeignKey('user.id'))

    @property
    def path(self):
        """
        Path of the photo on the server.
        """
        return f'./photos/{self.filename}'

    def has_read_permission(self, other_user: User) -> bool:
        """
        Checks if the other user has permission to view that photo.
        """
        # pylint: disable=no-member
        return self.user.has_general_read_permission(other_user)
