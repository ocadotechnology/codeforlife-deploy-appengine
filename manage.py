#!/usr/bin/env python
import os
import sys

import kubernetes

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_site.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

    kubernetes.config.load_kube_config("django_site/kubeconfig.yaml")
