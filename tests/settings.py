try:
    import honeypot
except ImportError:
    honeypot = None

SECRET_KEY = 'thisisntactuallysecretatall'

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django_nose',
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

SITE_ID = 1

ROOT_URLCONF = 'tests.urls'

HONEYPOT_FIELD_NAME = 'email2'

PASSWORD_HASHERS = {
    'django.contrib.auth.hashers.MD5PasswordHasher',
}

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
