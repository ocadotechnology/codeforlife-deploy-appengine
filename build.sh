#!/bin/bash -ex

export ENVIRONMENT="$1"

rbenv rehash
pip install beautifulsoup4
pip install requests
pip install -t lib requests-toolbelt

pip install -t lib codeforlife-portal
pip install -t lib git+https://github.com/ocadotechnology/aimmo.git@change_bundling_order
#if [ "$ENVIRONMENT" = "default" ]
#then
#    pip install -t lib --upgrade --no-deps aimmo
#else
#    pip install -t lib --pre --upgrade --no-deps aimmo
#fi

python install_gaerpytz.py

./manage.py collectstatic --noinput
