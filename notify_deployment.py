#!/usr/bin/env python

import argparse
import logging
import os
from collections import defaultdict

import requests

logging.basicConfig()

MODULE_NAME = os.environ.get("MODULE_NAME")
PORTAL_BRANCH = os.environ.get("PORTAL_BRANCH")
RAPID_ROUTER_BRANCH = os.environ.get("RAPID_ROUTER_BRANCH")

success = True

parser = argparse.ArgumentParser()
parser.add_argument("success", nargs="?", default="true")
args = parser.parse_args()

if args.success.lower() in ["false", "0"]:
    success = False

message = f"<https://github.com/ocadotechnology/codeforlife-deploy-appengine/deployments|Deployment to {MODULE_NAME}> "
if success:
    versions = defaultdict(lambda: "error")
    try:
        versions = requests.get(
            f"https://{MODULE_NAME}-dot-decent-digit-629.appspot.com/versions/"
        ).json()
    except:
        logging.exception("Error occurred while getting versions")

    if PORTAL_BRANCH:
        versions["codeforlife-portal"] = PORTAL_BRANCH
    if RAPID_ROUTER_BRANCH:
        versions["rapid-router"] = RAPID_ROUTER_BRANCH

    message += (
        f"completed successfully :tada:\n"
        f"\n"
        f"codeforlife-portal: `{versions['codeforlife-portal']}`\n"
        f"rapid-router: `{versions['rapid-router']}`"
    )
else:
    message += "failed :boom:"

requests.post(os.environ["DEPLOY_NOTIFY_URL"], json={"text": message})
