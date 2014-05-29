"""
Unit tests runner for ``uppsell`` based on bundled example project.
Tests are independent from this example application but setuptools need
instructions how to interpret ``test`` command when we run::

    python setup.py test

"""
import os
import sys
import django

os.environ["DJANGO_SETTINGS_MODULE"] = 'uppsell.tests.settings'
from uppsell.tests import settings

settings.INSTALLED_APPS = (
    'uppsell',
)
settings.PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
)

def run_tests(settings):
    from django.test.utils import get_runner

    import django
    if hasattr(django, 'setup'):
        django.setup()

    TestRunner = get_runner(settings)
    test_runner = TestRunner(interactive=False, verbosity=2)
    failures = test_runner.run_tests([])
    return failures

def main():
    failures = run_tests(settings)
    sys.exit(failures)

if __name__ == '__main__':
    main()
