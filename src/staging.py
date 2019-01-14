# src/staging.py
# Settings used only in Travis staging

from .defaults import *

DEBUG = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'NAME': 'test',
        'USER': 'admin',
        'PASSWORD': 'YES',
    }
}

# other development specific settings
