#!/usr/bin/env python

import argparse
import os
import requests

MODULE_NAME = os.environ.get("MODULE_NAME")

failed = False

parser = argparse.ArgumentParser()
parser.add_argument("failed", nargs="?", default="0")
args = parser.parse_args()

if args.failed.lower() in ["1", "true"]:
    failed = True

message = f"<https://github.com/ocadotechnology/codeforlife-deploy-appengine/deployments|Deployment to {MODULE_NAME}> "
if failed:
    message += "failed :boom:"
else:
    message += "completed successfully :tada:"

print(message)
requests.post(os.environ["DEPLOY_NOTIFY_URL"], json={"text": message})
