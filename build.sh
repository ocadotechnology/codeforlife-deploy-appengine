#!/bin/bash -ex

gem install sass --version 3.3.4
rbenv rehash

pip install -t lib codeforlife-portal aimmo

./manage.py collectstatic --noinput

