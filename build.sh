#!/bin/bash -ex

export ENVIRONMENT="$1"

rbenv rehash
pip install requests
pip install -t lib requests-toolbelt

pip install -t lib git+https://github.com/ocadotechnology/django-autoconfig
pip install -t lib --upgrade git+https://github.com/ocadotechnology/codeforlife-portal@newsletter_consent_data

pip install -t lib django-anymail[amazon_ses]
pip install -t lib google-auth==1.*

if [ "$ENVIRONMENT" = "default" ]
then
    pip install -t lib --upgrade --no-deps aimmo
else
    pip install -t lib --pre --upgrade --no-deps aimmo
fi

python generate_requirements.py

./manage.py collectstatic --noinput
