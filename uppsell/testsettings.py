import os

DEBUG = False

INSTALLED_APPS = (
    'uppsell',
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

