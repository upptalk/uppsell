import os
from django.conf.global_settings import *

DEBUG = False

INSTALLED_APPS = (
    'uppsell',
    'djcelery',
)

TEST_RUNNER = 'django.test.simple.DjangoTestSuiteRunner'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'TEST_NAME': ':memory:',
    },
}

TEMPLATE_DIRS = (
)

SECRET_KEY = '-----------------------TEST-----------------------'

