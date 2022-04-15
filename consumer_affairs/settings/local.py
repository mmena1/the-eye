from .common import *

LOGGING['handlers']['file'] = {
    'level': os.getenv('DJANGO_LOG_LEVEL', 'ERROR'),
    'class': 'logging.FileHandler',
    'filename': BASE_DIR / 'the_eye' / 'logs' / 'server.log',
}

LOGGING['root']['handlers'].append('file')
