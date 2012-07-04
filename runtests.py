import os

from django.conf import settings

try:
    import honeypot
except ImportError:
    honeypot = None


def make_absolute_path(path):
    return os.path.join(os.path.realpath(os.path.dirname(__file__)), path)


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
        TEMPLATE_DIRS = (
            make_absolute_path('envelope/tests/templates'),
        ),
        ROOT_URLCONF = 'envelope.tests.urls',
        TEST_RUNNER = 'django_nose.NoseTestSuiteRunner',
        NOSE_ARGS = ['--stop'],
        HONEYPOT_FIELD_NAME = 'email2',
    )


from django.core.management import call_command

call_command('test', 'envelope')

