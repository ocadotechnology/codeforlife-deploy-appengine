from django_site.wsgi import application
import logging

LOGGER = logging.getLogger(__name__)

try:
    import googleclouddebugger

    LOGGER.info("got here")
    print("got here by print")
    googleclouddebugger.enable()
except ImportError:
    LOGGER.info("dammit")
    print("dammit by print")
    pass

app = application
