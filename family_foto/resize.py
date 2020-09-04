import flask_resize

from family_foto.config import Config

config = flask_resize.configuration.Config(
    url=Config.RESIZE_URL,
    root=Config.RESIZE_ROOT
)
resize = flask_resize.make_resizer(config)