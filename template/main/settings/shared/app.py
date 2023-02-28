"""
Django settings for {{ project_name }}.
"""
import logging
import os
import platform

from django.core.exceptions import ImproperlyConfigured

from mitol.common.envs import (
    get_bool,
    get_delimited_list,
    get_features,
    get_int,
    get_string,
    import_settings_modules,
)
from main.sentry import init_sentry

VERSION = "0.0.0"

import_settings_modules(
    "main.settings.shared.auth",
    "main.settings.shared.celery",
    "main.settings.shared.database",
    "main.settings.shared.storage",
)

SITE_ID = get_string(
    name="SITE_ID",
    default=1,
    description="The default site id for django sites framework",
)
ENVIRONMENT = get_string(
    name="ENVIRONMENT",
    default="dev",
    description="The execution environment that the app is in (e.g. dev, staging, prod)",
    required=True,
)

# this is only available to heroku review apps
HEROKU_APP_NAME = get_string(
    name="HEROKU_APP_NAME", default=None, description="The name of the review app"
)

# initialize Sentry before doing anything else so we capture any config errors
SENTRY_DSN = get_string(
    name="SENTRY_DSN", default="", description="The connection settings for Sentry"
)
SENTRY_LOG_LEVEL = get_string(
    name="SENTRY_LOG_LEVEL", default="ERROR", description="The log level for Sentry"
)
init_sentry(
    dsn=SENTRY_DSN,
    environment=ENVIRONMENT,
    version=VERSION,
    log_level=SENTRY_LOG_LEVEL,
    heroku_app_name=HEROKU_APP_NAME,
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

SITE_BASE_URL = get_string(
    name="SITE_BASE_URL",
    default=None,
    description="Base url for the application in the format PROTOCOL://HOSTNAME[:PORT]",
    required=True,
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_bool(
    name="DEBUG",
    default=False,
    dev_only=True,
    description="Set to True to enable DEBUG mode. Don't turn on in production.",
)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_string(
    name="SECRET_KEY", default=None, description="Django secret key.", required=True
)

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = get_delimited_list(
    name="CSRF_TRUSTED_ORIGINS",
    default=[],
    description="Comma separated string of trusted domains that should be CSRF exempt",
)

CORS_ALLOWED_ORIGINS = get_delimited_list(
    name="CORS_ALLOWED_ORIGINS",
    default=[],
    description="Comma separated string of trusted domains that should be allowed for CORS",
)

CORS_ALLOW_CREDENTIALS = get_bool(
    name="CORS_ALLOW_CREDENTIALS",
    default=True,
    description="Allow cookies to be sent in cross-site HTTP requests",
)

SECURE_SSL_REDIRECT = get_bool(
    name="SECURE_SSL_REDIRECT",
    default=True,
    description="Application-level SSL redirect setting.",
)

SECURE_SSL_HOST = get_string(
    name="SECURE_SSL_HOST",
    default=None,
    description="Hostname to redirect non-secure requests to. "
    "Overrides value from HOST header.",
)

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'server_status',
    # django-robots
    "robots",
    # Put our apps after this point
    "main",
    "accounts",
)

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django.contrib.sites.middleware.CurrentSiteMiddleware",
)

# enable the nplusone profiler only in debug mode
if DEBUG:
    INSTALLED_APPS += (
        'nplusone.ext.django',
    )
    MIDDLEWARE += (
        'nplusone.ext.django.NPlusOneMiddleware',
    )

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'main.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# django-robots
ROBOTS_USE_HOST = False
ROBOTS_CACHE_TIMEOUT = get_int(
    name="ROBOTS_CACHE_TIMEOUT",
    default=60 * 60 * 24,
    description="How long the robots.txt file should be cached",
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

# Serve static files with dj-static
STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Important to define this so DEBUG works properly
INTERNAL_IPS = (
    get_string(
        name="HOST_IP", default="127.0.0.1", description="This server's host IP"
    ),
)
# e-mail configurable admins
ADMIN_EMAIL = get_string(
    name="MITOL_ADMIN_EMAIL",
    default="",
    description="E-mail to send 500 reports to.",
    required=True,
)
if ADMIN_EMAIL != "":
    ADMINS = (("Admins", ADMIN_EMAIL),)
else:
    ADMINS = ()

# Logging configuration
LOG_LEVEL = get_string(
    name="MITOL_LOG_LEVEL", default="INFO", description="The log level default"
)
DJANGO_LOG_LEVEL = get_string(
    name="MITOL_DJANGO_LOG_LEVEL", default="INFO", description="The log level for django"
)

# For logging to a remote syslog host
LOG_HOST = get_string(
    name="LOG_HOST",
    default="localhost",
    description="Remote syslog server hostname",
)
LOG_HOST_PORT = get_int(
    name="LOG_HOST_PORT",
    default=514,
    description="Remote syslog server port",
)

HOSTNAME = platform.node().split('.')[0]

# nplusone profiler logger configuration
NPLUSONE_LOGGER = logging.getLogger('nplusone')
NPLUSONE_LOG_LEVEL = logging.ERROR

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'formatters': {
        'verbose': {
            'format': (
                '[%(asctime)s] %(levelname)s %(process)d [%(name)s] '
                '%(filename)s:%(lineno)d - '
                '[{hostname}] - %(message)s'
            ).format(hostname=HOSTNAME),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'syslog': {
            'level': LOG_LEVEL,
            'class': 'logging.handlers.SysLogHandler',
            'facility': 'local7',
            'formatter': 'verbose',
            'address': (LOG_HOST, LOG_HOST_PORT)
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'django': {
            'propagate': True,
            'level': DJANGO_LOG_LEVEL,
            'handlers': ['console', 'syslog'],
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': DJANGO_LOG_LEVEL,
            'propagate': True,
        },
        'nplusone': {
            'handlers': ['console'],
            'level': 'ERROR',
        }
    },
    'root': {
        'handlers': ['console', 'syslog'],
        'level': LOG_LEVEL,
    },
}

# server-status
STATUS_TOKEN = get_string(
    name="STATUS_TOKEN", default="", description="Token to access the status API."
)
HEALTH_CHECK = ['CELERY', 'REDIS', 'POSTGRES']

# django cache back-ends
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'local-in-memory-cache',
    },
    'redis': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": CELERY_BROKER_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
    },
}

FEATURES = get_features()

# django debug toolbar only in debug mode
if DEBUG:
    INSTALLED_APPS += ('debug_toolbar', )
    # it needs to be enabled before other middlewares
    MIDDLEWARE = (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ) + MIDDLEWARE