from flask_security import RoleMixin

from family_foto.models import db


class Role(db.Model, RoleMixin):
    """
    Access role of an user.
    """
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    users = db.Column('User', foreign_keys='User.roles')

    def __str__(self):
        return self.name
