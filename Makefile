.PHONY: test coverage

test:
	DJANGO_SETTINGS_MODULE=tests.settings django-admin.py test tests

coverage:
	DJANGO_SETTINGS_MODULE=tests.settings coverage run `which django-admin.py` test tests
	coverage html
