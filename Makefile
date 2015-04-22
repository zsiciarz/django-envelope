.PHONY: test coverage

test:
	export PYTHONPATH=`pwd` && \
	DJANGO_SETTINGS_MODULE=tests.settings django-admin.py test

coverage:
	export PYTHONPATH=`pwd` && \
	DJANGO_SETTINGS_MODULE=tests.settings coverage run `which django-admin.py` test
	coverage html
