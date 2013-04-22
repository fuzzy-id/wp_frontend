# -*- coding: utf-8 -*-
import os
import sys

from setuptools import setup, find_packages

_here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(_here, 'README.org')).read()
    CHANGES = open(os.path.join(_here, 'CHANGES.txt')).read()
except IOError:
    README = CHANGES = ''

INSTALL_REQUIRES = [
    'pyramid',
    'SQLAlchemy',
    'mysql-python',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'waitress',
    'WebTest',
    'deform',
    'matplotlib'
    ]

TESTS_REQUIRE = []
if sys.version_info < (2, 7):
    TESTS_REQUIRE.append('unittest2')

setup(name='wp_frontend',
      version='0.2a1',
      description='wp_frontend',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Thomas Bach',
      author_email='bachth@uni-mainz.de',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='wp_frontend.tests',
      install_requires = INSTALL_REQUIRES,
      tests_require=TESTS_REQUIRE,
      entry_points = """\
      [paste.app_factory]
      main = wp_frontend:main
      [console_scripts]
      initialize_wp_frontend_db = wp_frontend.scripts.initializedb:main
      """,
      )

