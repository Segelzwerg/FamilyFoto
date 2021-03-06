from sqlite3 import OperationalError
from typing import List
from typing import Optional

from family_foto.logger import log
from family_foto.models import db
from family_foto.models.role import Role
from family_foto.models.user import User
from family_foto.models.user_settings import UserSettings


# pylint: disable=unsubscriptable-object]
def add_user(username: str, password: str, roles: List[Role], active=False) -> Optional[User]:
    """
    This registers an user.
    :param username: name of the user
    :param password: plain text password
    :param roles: list of the roles the user has
    :param active: if the user is already activated
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
    user.active = active

    db.session.add(user_settings)
    db.session.add(user)
    try:
        db.session.commit()
        log.info(f'{user.username} registered.')
    except OperationalError as op_error:
        db.session.rollback()
        log.error(op_error)
        return None
    return user
