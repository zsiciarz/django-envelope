import logging
import os

import django

try:
    import honeypot
except ImportError:
    honeypot = None

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'thisisntactuallysecretatall'

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'envelope',
)

if honeypot:
    INSTALLED_APPS += ('honeypot',)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_DIRS = [
    os.path.join(BASE_DIR, 'tests', 'templates'),
]

ROOT_URLCONF = 'tests.urls'

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

HONEYPOT_FIELD_NAME = 'email2'

PASSWORD_HASHERS = {
    'django.contrib.auth.hashers.MD5PasswordHasher',
}

if django.VERSION[:2] < (1, 6):
    TEST_RUNNER = 'discover_runner.DiscoverRunner'

logging.getLogger('envelope').addHandler(logging.NullHandler())
