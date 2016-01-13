
import logging
import os
import sys

logging.error("sys.path: %s", sys.path)
logging.error("ls: %s", os.listdir('.')
logging.error("ls: %s", os.listdir('webapp')

try:
    import webapp.wsgi
except ImportError as err:
    logging.error("ImportError: %s", err)
    raise

application = webapp.wsgi.application
