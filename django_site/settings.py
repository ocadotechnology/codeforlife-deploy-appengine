"""
Django settings for codeforlife-deploy.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import json
# Build paths inside the project like this: rel(rel_path)
import os

from .permissions import is_cloud_scheduler

MODULE_NAME = os.getenv("MODULE_NAME")
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
DOTDIGITAL_AUTH = os.getenv("DOTDIGITAL_AUTH", "")

SECURE_HSTS_SECONDS = 31536000  # One year
SECURE_SSL_REDIRECT = True
SECURE_REDIRECT_EXEMPT = [r"^mail/weekly/$", r"^cron/.*"]

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Application definition

INSTALLED_APPS = (
    "deploy",
    "game",
    "pipeline",
    "portal",
    "django_recaptcha",
    "common",
    "django.contrib.admin",
    "django.contrib.admindocs",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "django_reverse_js",
    "import_export",
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
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "deploy.middleware.exceptionlogging.ExceptionLoggingMiddleware",
    "deploy.middleware.security.CustomSecurityMiddleware",
    "deploy.middleware.session_timeout.SessionTimeoutMiddleware",
    "django_otp.middleware.OTPMiddleware",
    "preventconcurrentlogins.middleware.PreventConcurrentLoginsMiddleware",
    "csp.middleware.CSPMiddleware",
    "deploy.middleware.screentime_warning.ScreentimeWarningMiddleware",
    "deploy.middleware.maintenance.MaintenanceMiddleware",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "portal.backends.StudentLoginBackend",
]

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_COOKIE_AGE = 60 * 60
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

ROOT_URLCONF = "django_site.urls"

WSGI_APPLICATION = "django_site.wsgi.application"

CSRF_FAILURE_VIEW = "deploy.views.csrf_failure"

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-gb"

LANGUAGES = (("en-gb", "English"),)

TIME_ZONE = "Europe/London"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_ROOT = rel("static") + "/email_media/"

PIPELINE_ENABLED = False  # True if assets should be compressed, False if not.

# Leaving an empty PIPELINE dict here so that the build doesn't complain about it not being initialised
PIPELINE = {}

# Gets all the static files from the apps mentioned above in INSTALLED_APPS
STATICFILES_FINDERS = ["django.contrib.staticfiles.finders.AppDirectoriesFinder"]

# Auth URLs

LOGIN_URL = "/login_form/"
LOGOUT_URL = "/logout/"
LOGIN_REDIRECT_URL = "/teach/dashboard/"

# Required for admindocs

SITE_ID = 1


# PRESENTATION LAYER

# Deployment

ALLOWED_HOSTS = [".appspot.com", ".codeforlife.education"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.getenv("DATABASE_HOST"),
        "NAME": os.getenv("DATABASE_NAME"),
        "USER": "postgres",
        "PASSWORD": os.getenv("DATABASE_PASSWORD"),
        "ATOMIC_REQUESTS": True,
    }
}

# Running on App Engine, so use additional settings
if os.getenv("GAE_APPLICATION", None):
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

    SOCIAL_AUTH_PANDASSO_KEY = "code-for-life"
    SOCIAL_AUTH_PANDASSO_SECRET = os.getenv("PANDASSO_SECRET")
    SOCIAL_AUTH_PANDASSO_REDIRECT_IS_HTTPS = True
    PANDASSO_URL = os.getenv("PANDASSO_URL")

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    CSRF_USE_SESSIONS = False

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
                "common.context_processors.module_name",
                "common.context_processors.cookie_management_enabled",
            ],
        },
    }
]

CMS_TEMPLATES = (("portal/base.html", "Template One"),)

IS_CLOUD_SCHEDULER_FUNCTION = is_cloud_scheduler
CLOUD_STORAGE_PREFIX = "https://storage.googleapis.com/codeforlife-assets/"

COOKIE_MANAGEMENT_ENABLED = True


def domain():
    """Returns the full domain depending on whether it's local, dev, staging or prod."""
    domain_name = "https://www.codeforlife.education"

    if MODULE_NAME == "local":
        domain_name = "localhost:8000"
    elif MODULE_NAME == "staging" or MODULE_NAME == "dev":
        domain_name = f"https://{MODULE_NAME}-dot-decent-digit-629.appspot.com"

    return domain_name


CSP_DEFAULT_SRC = ("self",)
CSP_CONNECT_SRC = (
    "'self'",
    "https://*.onetrust.com/",
    "https://api.pwnedpasswords.com",
    "https://euc-widget.freshworks.com/",
    "https://codeforlife.freshdesk.com/",
    "https://api.iconify.design/",
    "https://api.simplesvg.com/",
    "https://api.unisvg.com/",
    "https://www.google-analytics.com/",
    "https://region1.google-analytics.com/g/",
    "https://crowdin.com/",
    "https://stats.g.doubleclick.net/",
)
CSP_FONT_SRC = (
    "'self'",
    "https://fonts.gstatic.com/",
    "https://fonts.googleapis.com/",
    "https://use.typekit.net/",
)
CSP_SCRIPT_SRC = (
    "'self'",
    "'unsafe-inline'",
    "'unsafe-eval'",
    "https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.0.0/crypto-js.min.js",
    "https://cdn.crowdin.com/",
    "https://*.onetrust.com/",
    "https://code.jquery.com/",
    "https://euc-widget.freshworks.com/",
    "https://cdn-ukwest.onetrust.com/",
    "https://code.iconify.design/2/2.0.3/iconify.min.js",
    "https://www.googletagmanager.com/",
    "https://www.google-analytics.com/analytics.js",
    "https://www.recaptcha.net/",
    "https://www.google.com/recaptcha/",
    "https://www.gstatic.com/recaptcha/",
    "https://use.typekit.net/mrl4ieu.js",
    f"{domain()}/static/portal/",
    f"{domain()}/static/common/",
)
CSP_STYLE_SRC = (
    "'self'",
    "'unsafe-inline'",
    "https://euc-widget.freshworks.com/",
    "https://cdn-ukwest.onetrust.com/",
    "https://fonts.googleapis.com/",
    "https://code.jquery.com/ui/1.13.1/themes/base/jquery-ui.css",
    "https://cdn.crowdin.com/",
    f"{domain()}/static/portal/",
)
CSP_FRAME_SRC = (
    "https://storage.googleapis.com/",
    "https://2662351606-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/",
    "https://www.youtube-nocookie.com/",
    "https://www.recaptcha.net/",
    "https://www.google.com/recaptcha/",
    "https://crowdin.com/",
    f"{domain()}/static/common/img/",
    f"{domain()}/static/game/image/",
)
CSP_IMG_SRC = (
    "https://storage.googleapis.com/codeforlife-assets/images/",
    "https://cdn-ukwest.onetrust.com/",
    "https://p.typekit.net/",
    "https://cdn.crowdin.com/",
    "https://crowdin-static.downloads.crowdin.com/",
    "https://www.google-analytics.com/",
    "data:",
    f"{domain()}/static/portal/img/",
    f"{domain()}/static/portal/static/portal/img/",
    f"{domain()}/static/portal/img/",
    f"{domain()}/favicon.ico",
    f"{domain()}/img/",
    f"{domain()}/account/two_factor/qrcode/",
    f"{domain()}/static/",
    f"{domain()}/static/game/image/",
    f"{domain()}/static/game/raphael_image/",
    f"{domain()}/static/game/js/blockly/media/",
    f"{domain()}/static/icons/",
)
CSP_OBJECT_SRC = (f"{domain()}/static/common/img/", f"{domain()}/static/game/image/")
CSP_MEDIA_SRC = (
    f"{domain()}/static/game/sound/",
    f"{domain()}/static/game/js/blockly/media/",
    f"{domain()}/static/portal/video/",
)
CSP_MANIFEST_SRC = (f"{domain()}/static/manifest.json",)
