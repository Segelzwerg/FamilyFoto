import base64
import os
from datetime import datetime, timedelta

from family_foto.models import db


class AuthToken(db.Model):
    """
    Authentication Token
    """
    id = db.Column(db.Integer, primary_key=True, index=True, unique=True)
    token = db.Column(db.String(32), index=True, unique=True)
    expiration = db.Column(db.DateTime)

    @staticmethod
    def check(token: 'AuthToken') -> bool:
        """
        Checks if the an AuthToken is still valid.
        """
        return token.expiration < datetime.utcnow()

    @staticmethod
    def create_token(expires_in: int = 3600) -> 'AuthToken':
        """
        Generates a new AuthToken.
        :param expires_in: seconds until the token expires.
        """
        now = datetime.utcnow()
        token_string = base64.b64encode(os.urandom(24)).decode('utf-8')
        expiration = now + timedelta(seconds=expires_in)
        token = AuthToken(token=token_string, expiration=expiration)
        db.session.add(token)
        return token
