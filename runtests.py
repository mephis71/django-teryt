#!/usr/bin/env python
# coding: utf-8

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import sys

try:
    import django
    print("Django version: {}".format(django.get_version()))

    from django.conf import settings

    import environ
    env = environ.Env()

    settings.configure(
        DEBUG=True,
        USE_TZ=True,
        DATABASES={
            # Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
            'default': env.db(
                "DATABASE_URL",
                default="sqlite://:memory:"),
        },
        ROOT_URLCONF="teryt.urls",
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sites",
            "teryt",
        ],
        # To suppress Django 1.7 warning about changed defaults
        MIDDLEWARE_CLASSES=(
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware'
        ),
        SITE_ID=1,
    )
    django.setup()

except ImportError:
    raise ImportError("To fix this error, run: pip install -r requirements-test.txt")


def run_tests(*test_args):
    if not test_args:
        test_args = ['teryt.tests']
    # Run tests
    from django.test.utils import get_runner
    test_runner = get_runner(settings)()
    failures = test_runner.run_tests(test_args)
    if failures:
        sys.exit(failures)


if __name__ == '__main__':
    run_tests(*sys.argv[1:])
