# Minimal settings module required for running django-envelope's unit tests.

import os


def make_absolute_path(path):
    return os.path.join(os.path.realpath(os.path.dirname(__file__)), path)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django_nose',
    'envelope',
    'honeypot',
)

TEMPLATE_DIRS = (
    make_absolute_path('templates'),
)

ROOT_URLCONF = 'example_project.urls'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = ['--stop']

HONEYPOT_FIELD_NAME = 'email2'

