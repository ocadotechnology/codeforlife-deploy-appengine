#!/bin/bash -ex

export ENVIRONMENT="$1"

gem install sass --version 3.3.4
rbenv rehash
pip install beautifulsoup4
pip install requests
pip install requests-toolbelt

pip install -t lib codeforlife-portal
if [ "$ENVIRONMENT" = "default" ]
then
    pip install -t lib --upgrade --no-deps aimmo
else
    pip install -t lib --pre --upgrade --no-deps aimmo
fi

pip install urllib3==1.23

python install_gaerpytz.py

./manage.py collectstatic --noinput
