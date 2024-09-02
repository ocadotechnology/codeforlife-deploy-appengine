"""
Django settings for django-pipeline in codeforlife-deploy.
This file is used to compile the 3 CSS files we need for the site.
We have a whole separate file so that we can run collectstatic after all the other static files have been collected,
so that the source and output files are under the same parent folder. This is to avoid causing a SuspiciousFileOperation
error.
"""

# Build paths inside the project like this: rel(rel_path)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
rel = lambda rel_path: os.path.join(BASE_DIR, rel_path)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET", "NOT A SECRET")

DEBUG = True

# Application definition

INSTALLED_APPS = (
    "anymail",
    "deploy",
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
    "django_reverse_js",
    "rest_framework",
    "import_export",
    "django_otp",
    "django_otp.plugins.otp_static",
    "django_otp.plugins.otp_totp",
    "sekizai",  # for javascript and css management
    "treebeard",
    "two_factor",
    "preventconcurrentlogins",
)

# Static files (CSS, JavaScript, Images)

STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_ROOT = rel("static") + "/email_media/"

PIPELINE_ENABLED = False  # True if assets should be compressed, False if not.

PIPELINE = {
    "COMPILERS": ("portal.pipeline_compilers.LibSassCompiler",),
    "STYLESHEETS": {
        "css": {
            "source_filenames": (
                rel("static/portal/sass/bootstrap.scss"),
                rel("static/portal/sass/colorbox.scss"),
                rel("static/portal/sass/styles.scss"),
                rel("static/game/css/level_selection.css"),
                rel("static/game/css/backgrounds.css"),
            ),
            "output_filename": "portal.css",
        },
        "game-scss": {"source_filenames": (rel("static/game/sass/game.scss"),), "output_filename": "game.css"},
        "popup": {
            "source_filenames": (rel("static/portal/sass/partials/_popup.scss"),),
            "output_filename": "popup.css",
        },
    },
    "CSS_COMPRESSOR": None,
    "SASS_ARGUMENTS": "--quiet",
}

STATICFILES_FINDERS = ["pipeline.finders.PipelineFinder"]
STATICFILES_STORAGE = "pipeline.storage.PipelineStorage"

# We only need to look into these 2 folders
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static/portal/"), os.path.join(BASE_DIR, "static/game/")]
