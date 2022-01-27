import os
import logging
import time
from threading import Thread

import yaml
from kubernetes import config

CURR_DIR = os.path.abspath(os.path.dirname(__file__))

logging.basicConfig(level=logging.DEBUG)


def setup_gke():
    filename = os.path.join(CURR_DIR, "kubeconfig.yaml")
    config_dict = yaml.safe_load(open(filename, "r").read())
    config_reload_interval = 15 * 60  # 15 minutes

    def load_kube_config_indefinitely(interval):
        while True:
            try:
                logging.info("Loading kube config")
                config.load_kube_config_from_dict(config_dict)
            except:
                logging.exception("Exception when calling load_kube_config_from_dict")
            time.sleep(interval)

    # Start a thread that loads kube config periodically
    thread = Thread(
        target=load_kube_config_indefinitely,
        args=(config_reload_interval,),
        daemon=True,
    )
    thread.start()
