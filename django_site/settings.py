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

from aimmo.csp_config import *
from portal.csp_config import *
from game.csp_config import *

from .permissions import is_cloud_scheduler

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
rel = lambda rel_path: os.path.join(BASE_DIR, rel_path)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET", "NOT A SECRET")

RECAPTCHA_PRIVATE_KEY = os.getenv("RECAPTCHA_PRIVATE_KEY", "NOT A SECRET")
RECAPTCHA_PUBLIC_KEY = os.getenv("RECAPTCHA_PUBLIC_KEY", "NOT A SECRET")
NOCAPTCHA = True

DOTMAILER_CREATE_CONTACT_URL = os.getenv("DOTMAILER_CREATE_CONTACT_URL", "")
DOTMAILER_MAIN_ADDRESS_BOOK_URL = os.getenv("DOTMAILER_MAIN_ADDRESS_BOOK_URL", "")
DOTMAILER_TEACHER_ADDRESS_BOOK_URL = os.getenv("DOTMAILER_TEACHER_ADDRESS_BOOK_URL", "")
DOTMAILER_STUDENT_ADDRESS_BOOK_URL = os.getenv("DOTMAILER_STUDENT_ADDRESS_BOOK_URL", "")
DOTMAILER_NO_ACCOUNT_ADDRESS_BOOK_URL = os.getenv("DOTMAILER_NO_ACCOUNT_ADDRESS_BOOK_URL", "")
DOTMAILER_GET_USER_BY_EMAIL_URL = os.getenv("DOTMAILER_GET_USER_BY_EMAIL_URL", "")
DOTMAILER_DELETE_USER_BY_ID_URL = os.getenv("DOTMAILER_DELETE_USER_BY_ID_URL", "")
DOTMAILER_PUT_CONSENT_DATA_URL = os.getenv("DOTMAILER_PUT_CONSENT_DATA_URL", "")
DOTMAILER_SEND_CAMPAIGN_URL = os.getenv("DOTMAILER_SEND_CAMPAIGN_URL", "")
DOTMAILER_THANKS_FOR_STAYING_CAMPAIGN_ID = os.getenv("DOTMAILER_THANKS_FOR_STAYING_CAMPAIGN_ID", "")
DOTMAILER_USER = os.getenv("DOTMAILER_USER", "")
DOTMAILER_PASSWORD = os.getenv("DOTMAILER_PASSWORD", "")
DOTMAILER_DEFAULT_PREFERENCES = json.loads(os.getenv("DOTMAILER_DEFAULT_PREFERENCES", "[]") or "[]")

SECURE_HSTS_SECONDS = 31536000  # One year
SECURE_SSL_REDIRECT = True

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Application definition

INSTALLED_APPS = (
    "anymail",
    "deploy",
    "aimmo",
    "game",
    "pipeline",
    "portal",
    "captcha",
    "common",
    "django.contrib.admin",
    "django.contrib.admindocs",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "django_js_reverse",
    "rest_framework",
    "django_otp",
    "django_otp.plugins.otp_static",
    "django_otp.plugins.otp_totp",
    "sekizai",  # for javascript and css management
    "treebeard",
    "two_factor",
    "preventconcurrentlogins",
)

MIDDLEWARE = [
    "deploy.middleware.admin_access.AdminAccessMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "deploy.middleware.security.CustomSecurityMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "deploy.middleware.session_timeout.SessionTimeoutMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "deploy.middleware.exceptionlogging.ExceptionLoggingMiddleware",
    "django_otp.middleware.OTPMiddleware",
    "preventconcurrentlogins.middleware.PreventConcurrentLoginsMiddleware",
    "csp.middleware.CSPMiddleware",
    "deploy.middleware.screentime_warning.ScreentimeWarningMiddleware",
]

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_COOKIE_AGE = 60 * 60
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

ROOT_URLCONF = "django_site.urls"

WSGI_APPLICATION = "django_site.wsgi.application"

CSRF_FAILURE_VIEW = "deploy.views.csrf_failure"

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = "en-gb"

LANGUAGES = (("en-gb", "English"),)

TIME_ZONE = "Europe/London"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, "static")

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
    }
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": os.getenv("DATABASE_HOST"),
        "NAME": os.getenv("DATABASE_NAME"),
        "USER": "root",
    }
}

PIPELINE_ENABLED = True  # True if assets should be compressed, False if not.

PIPELINE = {
    "COMPILERS": ("portal.pipeline_compilers.LibSassCompiler",),
    "STYLESHEETS": {
        "css": {
            "source_filenames": (
                rel("static/portal/sass/bootstrap.scss"),
                rel("static/portal/sass/colorbox.scss"),
                rel("static/portal/sass/styles.scss"),
            ),
            "output_filename": "portal.css",
        },
        "game-scss": {
            "source_filenames": (
                rel("static/game/sass/game.scss"),
            ),
            "output_filename": "game.css",
        },
        "popup": {
            "source_filenames": (
                rel("static/portal/sass/partials/_popup.scss"),
            ),
            "output_filename": "popup.css",
        },
    },
    "CSS_COMPRESSOR": None,
    "SASS_ARGUMENTS": "--quiet",
}

STATICFILES_FINDERS = ["pipeline.finders.PipelineFinder", "django.contrib.staticfiles.finders.FileSystemFinder"]
STATICFILES_STORAGE = "pipeline.storage.PipelineStorage"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "lib/portal/static/"),
    os.path.join(BASE_DIR, "lib/game/static/"),
    os.path.join(BASE_DIR, "lib/aimmo/static/"),
    os.path.join(BASE_DIR, "lib/common/static/"),
    os.path.join(BASE_DIR, "lib/deploy/static/"),
    os.path.join(BASE_DIR, "lib/treebeard/static/"),
    os.path.join(BASE_DIR, "lib/django_countries/static/"),
    os.path.join(BASE_DIR, "lib/rest_framework/static/"),
]

# Running on App Engine, so use additional settings
if os.getenv("GAE_APPLICATION", None):
    MODULE_NAME = os.getenv("MODULE_NAME")

    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": f"redis://{os.getenv('REDIS_IP')}:{os.getenv('REDIS_PORT')}/0",
            "KEY_PREFIX": os.getenv("CACHE_PREFIX"),
            "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        }
    }
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
    f"/game-{game}/socket.io",
)


AIMMO_GAME_SERVER_PORT_FUNCTION = lambda game: 0


AIMMO_GAME_SERVER_SSL_FLAG = True

IS_CLOUD_SCHEDULER_FUNCTION = is_cloud_scheduler
CLOUD_STORAGE_PREFIX = "https://storage.googleapis.com/codeforlife-assets/"
