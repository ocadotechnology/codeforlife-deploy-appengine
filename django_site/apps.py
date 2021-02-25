import os

import yaml
from kubernetes import config

CURR_DIR = os.path.abspath(os.path.dirname(__file__))


def setup_gke():
    filename = os.path.join(CURR_DIR, "kubeconfig.yaml")
    config_dict = yaml.safe_load(open(filename, "r").read())
    config.load_kube_config_from_dict(config_dict)
