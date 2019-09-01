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

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': (
            os.path.join(BASE_DIR, 'tests', 'templates'),
        ),
        'OPTIONS': {
            'context_processors': (
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ),
        },
    }
]

ROOT_URLCONF = 'tests.urls'

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

HONEYPOT_FIELD_NAME = 'email2'

PASSWORD_HASHERS = {
    'django.contrib.auth.hashers.MD5PasswordHasher',
}

logging.getLogger('envelope').addHandler(logging.NullHandler())
