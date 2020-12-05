import logging
import os
from logging.config import dictConfig

LOG_FILE_NAME = 'server_werkzeug.log'
LOG_PATH = os.path.join('instance', 'log')

if not os.path.exists(LOG_PATH):
    os.mkdir('instance')
    os.mkdir(LOG_PATH)

    with open(f'{LOG_PATH}/{LOG_FILE_NAME}', 'w+'):
        pass

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': f'{LOG_PATH}/{LOG_FILE_NAME}',
            'maxBytes': 1024,
            'backupCount': 5,
            'level': 'DEBUG',
            'formatter': 'default'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi', 'file']
    }
})

log = logging
