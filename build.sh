#!/bin/bash

pip install -t lib codeforlife-portal

./manage.py collectstatic --noinput

