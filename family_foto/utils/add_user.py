from family_foto.logger import log
from family_foto.models import db
from family_foto.models.role import Role
from family_foto.models.user import User
from family_foto.models.user_settings import UserSettings


def add_user(username: str, password: str, roles: [Role]) -> User:
    """
    This registers an user.
    :param username: name of the user
    :param password: plain text password
    :param roles: list of the roles the user has
    """
    user = User(username=username)
    user.set_password(password)
    exists = User.query.filter_by(username=username).first()
    if exists:
        log.warning(f'{user.username} already exists.')
        return exists

    user_settings = UserSettings(user_id=user.id)
    user.settings = user_settings
    user.roles = roles
    user.active = False

    db.session.add(user_settings)
    db.session.add(user)
    db.session.commit()
    log.info(f'{user.username} registered.')
    return user
