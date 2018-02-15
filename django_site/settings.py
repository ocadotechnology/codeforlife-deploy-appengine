"""
Django settings for codeforlife-deploy.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

from django.core.urlresolvers import reverse_lazy

# Build paths inside the project like this: rel(rel_path)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
rel = lambda rel_path: os.path.join(BASE_DIR, rel_path)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET', 'NOT A SECRET')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

# Application definition

INSTALLED_APPS = (
    'casper',
    'deploy',
    'portal',
    'reports',
    'game',
    'djangocms_admin_style',  # for the admin skin. You **must** add 'djangocms_admin_style' in the list **before** 'django.contrib.admin'.
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_countries',
    'django_forms_bootstrap',
    'rest_framework',
    'online_status',

    #CMS
    'cms',  # django CMS itself
    'treebeard',
    'menus',  # helper for model independent hierarchical website navigation
    'sekizai',  # for javascript and css management

    # CMS Plugins
    'djangocms_file',
    'djangocms_flash',
    'djangocms_googlemap',
    'djangocms_inherit',
    'djangocms_picture',
    'djangocms_teaser',
    'djangocms_video',
    'djangocms_link',
    'djangocms_snippet',
    'djangocms_text_ckeditor',  # note this needs to be above the 'cms' entry
    'reversion',
    'players',
)

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'online_status.middleware.OnlineStatusMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'deploy.middleware.exceptionlogging.ExceptionLoggingMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
    'portal.middleware.ratelimit_login_attempts.RateLimitLoginAttemptsMiddleware',
]

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_COOKIE_AGE = 60 * 60
SESSION_SAVE_EVERY_REQUEST = True

ROOT_URLCONF = 'django_site.urls'

WSGI_APPLICATION = 'django_site.wsgi.application'

CSRF_FAILURE_VIEW = 'deploy.views.csrf_failure'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-gb'

LANGUAGES = (('en-gb', 'English'),)

TIME_ZONE = 'Europe/London'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = rel('static')

MEDIA_ROOT = rel('static')+'/email_media/'

# Auth URLs

LOGIN_URL = '/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = reverse_lazy('portal.views.teacher.dashboard.dashboard_manage')

# Required for admindocs

SITE_ID = 1


# PRESENTATION LAYER

# Deployment

ALLOWED_HOSTS = ['.appspot.com', '.codeforlife.education']

if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine'):
    # Running on production App Engine, so use a Google Cloud SQL database.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '/cloudsql/decent-digit-629:db',
            'NAME': os.getenv('DATABASE_NAME'),
            'USER': 'root',
        }
    }
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'KEY_PREFIX': os.getenv('CACHE_PREFIX'),
        }
    }
    PIPELINE_ENABLED = True
    # inject the lib folder into the python path
    import sys
    lib_path = os.path.join(os.path.dirname(__file__), 'lib')
    if lib_path not in sys.path:
        sys.path.append(lib_path)
    # setup email on app engine
    EMAIL_BACKEND = 'deploy.mail.EmailBackend'
    # Specify a queue name for the async. email backend.
    EMAIL_QUEUE_NAME = 'default'
    MIDDLEWARE_CLASSES.insert(0, 'google.appengine.ext.appstats.recording.AppStatsDjangoMiddleware')

    SOCIAL_AUTH_PANDASSO_KEY = 'code-for-life'
    SOCIAL_AUTH_PANDASSO_SECRET = os.getenv('PANDASSO_SECRET')
    SOCIAL_AUTH_PANDASSO_REDIRECT_IS_HTTPS = True
    PANDASSO_URL = os.getenv('PANDASSO_URL')

    SESSION_COOKIE_SECURE = True
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': os.getenv('CLOUD_SQL_HOST'),
            'NAME': os.getenv('DATABASE_NAME'),
            'USER': 'root',
            'PASSWORD': os.getenv('CLOUD_SQL_PASSWORD'),
            'OPTIONS': {
                'ssl': {
                    'ca': 'server-ca.pem',
                    'cert': 'client-cert.pem',
                    'cipher': 'AES128-SHA',
                    'key': 'client-key.pem',
                }
            }
        }
    }
    PIPELINE_ENABLED = True

EMAIL_ADDRESS = 'no-reply@codeforlife.education'

LOCALE_PATHS = (
    'conf/locale',
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ()
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
            os.path.join(BASE_DIR, "templates"),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug' : TEMPLATE_DEBUG,
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'sekizai.context_processors.sekizai',
                'cms.context_processors.cms_settings',
            ],
        },
    },
]

CMS_TEMPLATES = (
    ('portal/base.html', 'Template One'),
)

MIGRATION_MODULES = {
    'menus': 'menus.migrations_django',

    # Add also the following modules if you're using these plugins:
    'djangocms_file': 'djangocms_file.migrations_django',
    'djangocms_flash': 'djangocms_flash.migrations_django',
    'djangocms_googlemap': 'djangocms_googlemap.migrations_django',
    'djangocms_inherit': 'djangocms_inherit.migrations_django',
    'djangocms_link': 'djangocms_link.migrations_django',
    'djangocms_picture': 'djangocms_picture.migrations_django',
    'djangocms_snippet': 'djangocms_snippet.migrations_django',
    'djangocms_teaser': 'djangocms_teaser.migrations_django',
    'djangocms_video': 'djangocms_video.migrations_django',
}


def get_module_name():
    return os.getenv('MODULE_NAME')


AIMMO_GAME_SERVER_URL_FUNCTION = lambda game: (os.getenv('MODULE_NAME') + '-aimmo.codeforlife.education',
                                               '/game-%s' % game)


AIMMO_GAME_SERVER_PORT_FUNCTION = lambda game: 0


AIMMO_GAME_SERVER_SSL_FLAG = True


# Keep this at the bottom
from django_autoconfig.autoconfig import configure_settings

configure_settings(globals())
