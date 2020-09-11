import os

basedir = os.path.abspath(os.path.dirname(__file__))


# pylint: disable=too-few-public-methods


class BaseConfig:
    """
    Basic configurations with all configuration have in common.
    """
    UPLOADED_PHOTOS_DEST = './photos'
    UPLOADED_VIDEOS_DEST = './videos'
    RESIZED_DEST = './resized-images'

    VIDEOS = tuple('mp4'.split())



class Config(BaseConfig):
    """
    Flask configuration.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'very-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, '../app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfiguration(BaseConfig):
    """
    Flask test configuration.
    """
    TESTING = True
    WTF_CSRF_ENABLED = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '../test.db')

    # Since we want our unit tests to run quickly
    # we turn this down - the hashing is still done
    # but the time-consuming part is left out.
    HASH_ROUNDS = 1

    UPLOADED_PHOTOS_DEST = './tests/photos'
    RESIZED_DEST = './tests/resized-images'
