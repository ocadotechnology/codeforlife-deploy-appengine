#!/bin/bash -ex

export ENVIRONMENT="$1"

rbenv rehash
pip install requests
pip install -t lib requests-toolbelt

pip install -t lib git+https://github.com/ocadotechnology/django-autoconfig
pip install -t lib --upgrade codeforlife-portal

pip install -t lib django-anymail[amazon_ses]
pip install -t lib google-auth==1.*

if [ "$ENVIRONMENT" = "default" ]
then
    pip install -t lib --upgrade --no-deps aimmo
else
    # pip install -t lib --pre --upgrade --no-deps aimmo
    # pip install -t lib --pre --upgrade --no-deps git+https://github.com/ocadotechnology/aimmo.git@agones2

    # Install agones from a branch
    git clone --depth 1 --branch agones2 https://github.com/ocadotechnology/aimmo.git
    pushd aimmo/game_frontend 
    yarn --frozen-lockfile
    NODE_ENV=production node djangoBundler.js
    popd
    pip install -t lib --pre --upgrade --no-deps ./aimmo
fi

python generate_requirements.py

./manage.py collectstatic --noinput
