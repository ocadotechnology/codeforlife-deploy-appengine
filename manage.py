#!/usr/bin/env python
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_site.settings")

    from django.core.management import execute_from_command_line

    # Need to setup GKE if running migrations
    if sys.argv[1] == "migrate":
        import kubernetes

        kubernetes.config.load_kube_config("/home/runner/.kube/config")

    execute_from_command_line(sys.argv)
