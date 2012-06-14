# This is our very stripped down settings, we have no UI, no admin nothin'.
from funfactory.settings_base import *

PROJECT_MODULE = 'solitude'
MINIFY_BUNDLES = {}

# Defines the views served for root URLs.
ROOT_URLCONF = '%s.urls' % PROJECT_MODULE

INSTALLED_APPS = (
    'funfactory',
    'django_nose',
    'lib.buyers',
    'lib.sellers',
    'lib.transactions',
    'solitude'
)

TEST_RUNNER = 'test_utils.runner.RadicalTestSuiteRunner'

MIDDLEWARE_CLASSES = (
    'django.middleware.transaction.TransactionMiddleware',
    'django.middleware.common.CommonMiddleware'
)

SESSION_COOKIE_SECURE = True
LOGGING = dict(loggers=dict(playdoh = {'level': logging.DEBUG}))

# PayPal values.
PAYPAL_APP_ID = ''
PAYPAL_AUTH = {'USER': '', 'PASSWORD': '', 'SIGNATURE': ''}
PAYPAL_CHAINS = ()
PAYPAL_CERT = None
PAYPAL_URL_WHITELIST = ()
PAYPAL_USE_SANDBOX = True
