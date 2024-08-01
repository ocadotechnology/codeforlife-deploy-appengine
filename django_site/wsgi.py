"""
WSGI config for codeforlife-portal project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import logging
import google.cloud.logging
from google.auth.exceptions import DefaultCredentialsError

logging.basicConfig(level=logging.DEBUG)

try:
    logging_client = google.cloud.logging.Client()
    logging_client.get_default_handler()
    logging_client.setup_logging()
except DefaultCredentialsError:
    logging.info("No google credentials provided, not connecting google logging client")


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_site.settings")

from lib.django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
