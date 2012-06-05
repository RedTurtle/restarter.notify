import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

requires = [
    'pyramid',
    'pyramid_celery',
    'pyramid_mailer',
    'PasteScript',
    'waitress',
    'requests',
    'celery-with-redis',
    'celerymon'
    ]

setup(name='restarter.notify',
      version='1.0',
      description='restarter notification package',
      long_description=README,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      namespace_packages=['restarter'],
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="restarter.notify",
      entry_points = """\
      [paste.app_factory]
      main = restarter.notify:main
      """,
      )

