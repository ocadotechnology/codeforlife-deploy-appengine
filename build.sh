#!/bin/bash -ex

export ENVIRONMENT="$1"

rbenv rehash
pip install requests
pip install -t lib requests-toolbelt

pip install -t lib codeforlife-portal

pip install -t lib django-anymail[amazon_ses]

if [ "$ENVIRONMENT" = "default" ]
then
    pip install -t lib --upgrade --no-deps aimmo
else
    pip install -t lib --pre --upgrade --no-deps git+https://github.com/ocadotechnology/aimmo@start_timer_if_no_players
fi

python generate_requirements.py

./manage.py collectstatic --noinput
