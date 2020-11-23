#!/bin/bash -ex

export ENVIRONMENT="$1"

rbenv rehash
pip install requests
pip install -t lib requests-toolbelt

pip install django-autoconfig

pip install -t lib --upgrade git+https://github.com/ocadotechnology/codeforlife-portal@django_2_upgrade
pip install -t lib --upgrade git+https://github.com/ocadotechnology/rapid-router@django_2_upgrade

pip install -t lib django-anymail[amazon_ses]
pip install -t lib google-auth==1.*

if [ "$ENVIRONMENT" = "default" ]
then
    pip install -t lib --upgrade --no-deps aimmo
else
    pip install -t lib --pre --upgrade --no-deps git+https://github.com/ocadotechnology/aimmo@django_2_upgrade
fi

pip install -t lib --upgrade "git+https://github.com/ocadotechnology/codeforlife-portal@django_2_upgrade#egg=cfl-common&subdirectory=cfl_common"

python generate_requirements.py

./manage.py collectstatic --noinput
