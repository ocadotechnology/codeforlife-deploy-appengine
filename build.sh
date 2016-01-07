#!/bin/bash -ex

gem install sass --version 3.3.4

pip install -t lib codeforlife-portal

./manage.py collectstatic --noinput

