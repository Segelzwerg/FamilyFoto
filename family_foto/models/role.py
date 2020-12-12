from family_foto.models import db


# pylint: disable = too-few-public-methods
class Role(db.Model):
    """
    Access role of an user.
    """
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    level = db.Column(db.Integer(), nullable=False)

    def __str__(self) -> str:
        return str(self.name)
