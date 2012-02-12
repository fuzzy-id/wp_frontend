import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.org')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'waitress',
    'WebTest',
    'deform',
    'matplotlib'
    ]

setup(name='wp_frontend',
      version='0.1',
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
      test_suite='wp_frontend',
      install_requires = requires,
      entry_points = """\
      [paste.app_factory]
      main = wp_frontend:main
      [console_scripts]
      populate_pyramid_start_alchemy = pyramid_start_alchemy.scripts.populate:main
      """,
      )

