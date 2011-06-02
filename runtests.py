import os
import sys

sys.path.insert(0, os.path.abspath('.'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_settings'

from django.conf import settings
from django.core.management import call_command

call_command('test', 'envelope')

