from django.conf import settings

try:
    import honeypot
except ImportError:
    honeypot = None


if not settings.configured:
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
    settings.configure(
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS = INSTALLED_APPS,
        SITE_ID = 1,
        ROOT_URLCONF = 'envelope.tests.urls',
        HONEYPOT_FIELD_NAME = 'email2',
    )


import django
try:
    django.setup()  # Django 1.7+
except AttributeError:
    pass

from django_nose import NoseTestSuiteRunner

test_runner = NoseTestSuiteRunner()
test_runner.run_tests(['envelope'])
