#!/usr/bin/env python
import os
import sys
import logging

LOGGER = logging.getLogger(__name__)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))

if __name__ == "__main__":
    try:
        import googleclouddebugger
        LOGGER.info("got here")
        print("got here by print")
        googleclouddebugger.enable()
    except ImportError:
        LOGGER.info("dammit")
        print("dammit by print")
        pass

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_site.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
