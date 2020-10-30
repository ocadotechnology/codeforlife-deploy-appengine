"""
Django settings for codeforlife-deploy.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: rel(rel_path)
import os
import json
from .permissions import is_cloud_scheduler

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
rel = lambda rel_path: os.path.join(BASE_DIR, rel_path)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET", "NOT A SECRET")

RECAPTCHA_PRIVATE_KEY = os.getenv("RECAPTCHA_PRIVATE_KEY", "NOT A SECRET")
RECAPTCHA_PUBLIC_KEY = os.getenv("RECAPTCHA_PUBLIC_KEY", "NOT A SECRET")
NOCAPTCHA = True

DOTMAILER_URL = os.getenv("DOTMAILER_URL", "")
DOTMAILER_USER = os.getenv("DOTMAILER_USER", "")
DOTMAILER_PASSWORD = os.getenv("DOTMAILER_PASSWORD", "")
DOTMAILER_DEFAULT_PREFERENCES = json.loads(
    os.getenv("DOTMAILER_DEFAULT_PREFERENCES", "[]") or "[]"
)

SECURE_HSTS_SECONDS = 31536000  # One year
SECURE_SSL_REDIRECT = True

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Application definition

INSTALLED_APPS = (
    "anymail",
    "deploy",
    "portal",
    "captcha",
    "game",
    #'djangocms_admin_style',  # for the admin skin. You **must** add 'djangocms_admin_style' in the list **before** 'django.contrib.admin'.
    "django.contrib.admin",
    "django.contrib.admindocs",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django_countries",
    "rest_framework",
    "treebeard",
    "sekizai",  # for javascript and css management
    "aimmo",
)

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "deploy.middleware.exceptionlogging.ExceptionLoggingMiddleware",
]

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_COOKIE_AGE = 60 * 60
SESSION_SAVE_EVERY_REQUEST = True

ROOT_URLCONF = "django_site.urls"

WSGI_APPLICATION = "django_site.wsgi.application"

CSRF_FAILURE_VIEW = "deploy.views.csrf_failure"

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = "en-gb"

LANGUAGES = (("en-gb", "English"), ("tr", "Turkish"))

TIME_ZONE = "Europe/London"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = "/static/"

STATIC_ROOT = rel("static")

MEDIA_ROOT = rel("static") + "/email_media/"

# Auth URLs

LOGIN_URL = "/login_form/"
LOGOUT_URL = "/logout/"
LOGIN_REDIRECT_URL = "/teach/dashboard/"

# Required for admindocs

SITE_ID = 1


# PRESENTATION LAYER

# Deployment

ALLOWED_HOSTS = [".appspot.com", ".codeforlife.education"]

ANYMAIL = {
    "AMAZON_SES_CLIENT_PARAMS": {
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "region_name": "eu-west-1",
    },
}

if os.getenv("GAE_APPLICATION", None):
    MODULE_NAME = os.getenv("MODULE_NAME")

    # Running on production App Engine, so use a Google Cloud SQL database.
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "HOST": "/cloudsql/decent-digit-629:europe-west1:db",
            "NAME": os.getenv("DATABASE_NAME"),
            "USER": "root",
        }
    }
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": f"redis://{os.getenv('REDIS_IP')}:{os.getenv('REDIS_PORT')}/0",
            "KEY_PREFIX": os.getenv("CACHE_PREFIX"),
            "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        }
    }
    PIPELINE_ENABLED = True
    # inject the lib folder into the python path
    import sys

    lib_path = os.path.join(os.path.dirname(__file__), "lib")
    if lib_path not in sys.path:
        sys.path.append(lib_path)
    # setup email on app engine
    EMAIL_BACKEND = "anymail.backends.amazon_ses.EmailBackend"

    SOCIAL_AUTH_PANDASSO_KEY = "code-for-life"
    SOCIAL_AUTH_PANDASSO_SECRET = os.getenv("PANDASSO_SECRET")
    SOCIAL_AUTH_PANDASSO_REDIRECT_IS_HTTPS = True
    PANDASSO_URL = os.getenv("PANDASSO_URL")

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "HOST": os.getenv("CLOUD_SQL_HOST"),
            "NAME": os.getenv("DATABASE_NAME"),
            "USER": "root",
            "PASSWORD": os.getenv("CLOUD_SQL_PASSWORD"),
            "OPTIONS": {
                "ssl": {
                    "ca": "server-ca.pem",
                    "cert": "client-cert.pem",
                    "cipher": "AES128-SHA",
                    "key": "client-key.pem",
                }
            },
        }
    }
    PIPELINE_ENABLED = True

EMAIL_ADDRESS = "no-reply@codeforlife.education"

LOCALE_PATHS = ("conf/locale",)

REST_FRAMEWORK = {"DEFAULT_AUTHENTICATION_CLASSES": ()}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            # insert your TEMPLATE_DIRS here
            os.path.join(BASE_DIR, "templates")
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "debug": DEBUG,
            "context_processors": [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "sekizai.context_processors.sekizai",
                "portal.context_processors.process_newsletter_form",
            ],
        },
    }
]

CMS_TEMPLATES = (("portal/base.html", "Template One"),)


AIMMO_GAME_SERVER_URL_FUNCTION = lambda game: (
    f"{os.getenv('GAE_SERVICE')}-aimmo.codeforlife.education",
    "/game-%s" % game,
)


AIMMO_GAME_SERVER_PORT_FUNCTION = lambda game: 0


AIMMO_GAME_SERVER_SSL_FLAG = True

IS_CLOUD_SCHEDULER_FUNCTION = is_cloud_scheduler

# Keep this at the bottom
from django_autoconfig.autoconfig import configure_settings

configure_settings(globals())
