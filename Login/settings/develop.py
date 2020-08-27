from .base import *

ALLOWED_HOSTS = ['*']

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'weixin',
        'USER': 'root',
        'PASSWORD': "123456",
        'HOST': 'localhost',
        "PORT": '3306',
    }
}


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': [
            '127.0.0.1:11211',
        ],
        'TIMEOUT': 60 * 60 * 3,
        'OPTIONS': {
            'server_max_value_length': 1024 * 1024 * 16,
        },
        'KEY_PREFIX': 'default'
    }
}