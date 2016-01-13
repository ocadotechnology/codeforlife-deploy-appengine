
import logging
import os
import sys

logging.error("sys.path: %s", sys.path)
logging.error("ls: %s", os.listdir('.'))
logging.error("ls: %s", os.listdir('lib'))


import django_site.wsgi

application = django_site.wsgi.application
