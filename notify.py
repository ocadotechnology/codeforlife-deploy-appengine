#!/usr/bin/env python

from __future__ import print_function

import os
import requests

APP_ID = os.environ['APP_ID']

staging_versions = requests.get("https://staging-dot-%s.appspot.com/versions/" % APP_ID).json()
prod_versions = requests.get("https://%s.appspot.com/versions/" % APP_ID).json()

message = '<https://snap-ci.com/ocadotechnology/codeforlife-deploy-appengine/branch/master|Staging deployment #%s> completed successfully.' % os.environ['SNAP_PIPELINE_COUNTER']

notify = False

for app_id, app_name in [
    ('rapid-router', 'Rapid Router'),
    ('codeforlife-portal', 'Portal'),
]:
    if staging_versions[app_id] == prod_versions[app_id]:
        message += '\n<https://github.com/ocadotechnology/%(app_id)s/compare/%(old_version)s...%(new_version)s|%(app_name)s changes>' % {
            'app_id': app_id,
            'app_name': app_name,
            'old_version': prod_versions[app_id],
            'new_version': staging_versions[app_id],
        }
        notify = True

if notify:
    print(message)
    requests.post(os.environ['DEPLOY_NOTIFY_URL'], json={'text': message})
