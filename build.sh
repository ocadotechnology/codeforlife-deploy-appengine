#!/bin/bash -ex

export ENVIRONMENT="$1"

rbenv rehash
pip install requests
pip install -t lib requests-toolbelt

#pip install -t lib git+https://github.com/ocadotechnology/django-autoconfig
pip install -t lib --upgrade codeforlife-portal

pip install -t lib django-anymail[amazon_ses]
pip install -t lib google-auth==1.*

if [ "$ENVIRONMENT" = "default" ]
then
    pip install -t lib --upgrade --no-deps aimmo
else
    pip install -t lib --pre --upgrade --no-deps aimmo

    # Uncomment the blocks below to install aimmo from a branch - don't forget to uncomment the line in generate_requirements.py too
    # git clone --depth 1 --branch agones3 https://github.com/ocadotechnology/aimmo.git

    # pushd aimmo
    # pip install wheel
    # ./aimmo_runner/build_worker_wheel.sh
    # popd

    # pushd aimmo/game_frontend
    # curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.37.2/install.sh | bash
    # export NVM_DIR="$HOME/.nvm"
    # [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
    # nvm install 12.20.2
    # nvm use 12.20.2
    # yarn --frozen-lockfile
    # NODE_ENV=production node djangoBundler.js
    # popd
    # pip install -t lib --pre --upgrade --no-deps ./aimmo
fi

python generate_requirements.py

./manage.py collectstatic --noinput
