from setuptools import setup, find_packages

setup(
    name='django-envelope',
    version='0.0.1',
    description='A contact form app for Django',
    author='Zbigniew Siciarz',
    author_email='antyqjon@gmail.com',
    install_requires=['Django', 'django-honeypot'],
    packages=find_packages(),
    include_package_data=True,
    classifiers=['Development Status :: 4 - Beta',
                 'Environment :: Web Environment',
                 'Framework :: Django',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Topic :: Utilities'],
)
