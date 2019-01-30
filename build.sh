#!/bin/bash -ex

export ENVIRONMENT="$1"

gem install sass --version 3.3.4
rbenv rehash
pip install git+https://github.com/PyGithub/PyGithub.git@ba50af5
pip install "urllib3==1.22" --force-reinstall

pip install -t lib codeforlife-portal
pip install -t lib git+https://github.com/ocadotechnology/aimmo.git@custom_metrics
# if [ "$ENVIRONMENT" = "default" ]
# then
#     pip install -t lib --upgrade --no-deps aimmo
# else
#     pip install -t lib --pre --upgrade --no-deps aimmo
# fi

python get_latest_aimmo_unity_release.py

rm -rf lib/pytz lib/pytz*.dist-info

./manage.py collectstatic --noinput