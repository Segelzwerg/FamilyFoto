from family_foto.models import db


class Approval(db.Model):
    """
    Database entity of approval request.
    """
    id = db.Column(db.Integer, index=True, primary_key=True, unique=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
