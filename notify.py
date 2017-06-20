#!/usr/bin/env python

from __future__ import print_function

import os
import requests

APP_ID = os.environ['APP_ID']

staging_versions = requests.get("https://staging-dot-%s.appspot.com/versions/" % APP_ID).json()
prod_versions = requests.get("https://%s.appspot.com/versions/" % APP_ID).json()

message = '<https://semaphoreci.com/celine/codeforlife-deploy-appengine|Deployment #%s> completed successfully.' % os.environ['SEMAPHORE_BUILD_NUMBER']

notify = False

for app_id, app_name in [
    ('rapid-router', 'Rapid Router'),
    ('codeforlife-portal', 'Portal'),
    ('aimmo', 'AI:MMO'),
]:
    if staging_versions.get(app_id, None) != prod_versions.get(app_id, None):
        message += '\n<https://github.com/ocadotechnology/%(app_id)s/compare/%(old_version)s...%(new_version)s|%(app_name)s changes>' % {
            'app_id': app_id,
            'app_name': app_name,
            'old_version': prod_versions.get(app_id, None),
            'new_version': staging_versions.get(app_id, None),
        }
        notify = True

#if notify:
message += ' wuhuhu testing things'
print(message)
requests.post(os.environ['DEPLOY_NOTIFY_URL'], json={'text': message})
