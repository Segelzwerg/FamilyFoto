from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


def create_session(app):
    engine = create_engine(app.config['DATABASE_URL_TEMPLATE'])
    session_factory = sessionmaker(bind=engine)
    # this is intentional to shadow the outer scope package
    # pylint: disable=invalid-name
    Session = scoped_session(session_factory)
    session = Session()
    return Session, session
