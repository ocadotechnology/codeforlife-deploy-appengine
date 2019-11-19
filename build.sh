#!/bin/bash -ex

export ENVIRONMENT="$1"

gem install sass --version 3.3.4
rbenv rehash
pip install git+https://github.com/PyGithub/PyGithub.git@ba50af5
pip install "urllib3==1.22" --force-reinstall

pip install -t lib codeforlife-portal
if [ "$ENVIRONMENT" = "default" ]
then
    pip install -t lib --upgrade --no-deps aimmo
else
    pip install -t lib --pre --upgrade --no-deps aimmo
fi

pip install beautifulsoup4

python install_gaerpytz.py

./manage.py collectstatic --noinput
