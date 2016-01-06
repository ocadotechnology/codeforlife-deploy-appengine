#!/bin/bash

pip install -t lib codeforlife-portal

./webapp/manage.py collectstatic --noinput

