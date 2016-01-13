
import logging
import sys

logging.error("sys.path: %s", sys.path)

try:
    import webapp.wsgi
except ImportError as err:
    logging.error("ImportError: %s", err)
    raise

application = webapp.wsgi.application
