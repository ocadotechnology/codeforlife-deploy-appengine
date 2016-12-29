#!/bin/bash -ex

gem install sass --version 3.3.4
rbenv rehash

pip install -t lib codeforlife-portal aimmo

rm -rf lib/pytz lib/pytz*.dist-info

./manage.py collectstatic --noinput

