#!/usr/bin/env python

import argparse
import os
import requests

MODULE_NAME = os.environ.get("MODULE_NAME")

success = True

parser = argparse.ArgumentParser()
parser.add_argument("success", nargs="?", default="true")
args = parser.parse_args()

if args.success.lower() in ["false", "0"]:
    success = False

message = f"<https://github.com/ocadotechnology/codeforlife-deploy-appengine/deployments|Deployment to {MODULE_NAME}> "
if success:
    message += "completed successfully :tada:"
else:
    message += "failed :boom:"

requests.post(os.environ["DEPLOY_NOTIFY_URL"], json={"text": message})
