import os
from .common import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': os.environ.get('POSTGRES_PORT'),
    }
}

RQ_QUEUES = {
    'default': {
        'HOST': 'redis', # Redis host needs to match the name in docker-compose.yml
        'PORT': 6379,
        'DB': 0,
        'DEFAULT_TIMEOUT': 60,
    },
}
