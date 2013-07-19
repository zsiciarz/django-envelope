import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-envelope',
    version=__import__('envelope').__version__,
    description='A contact form app for Django',
    long_description=read('README.rst'),
    author='Zbigniew Siciarz',
    author_email='antyqjon@gmail.com',
    url='http://github.com/zsiciarz/django-envelope',
    download_url='http://pypi.python.org/pypi/django-envelope',
    license='MIT',
    install_requires=['Django>=1.4'],
    packages=find_packages(exclude=['example_project']),
    include_package_data=True,
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Environment :: Web Environment',
                 'Framework :: Django',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 3',
                 'Topic :: Utilities'],
)
