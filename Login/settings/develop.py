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

