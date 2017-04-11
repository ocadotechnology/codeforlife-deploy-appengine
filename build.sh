#!/bin/bash -ex

gem install sass --version 3.3.4
rbenv rehash

pip install -t lib codeforlife-portal aimmo

rm -rf lib/pytz lib/pytz*.dist-info
rm -rf lib/djangocms_text_ckeditor lib/djangocms_text_ckeditor*.dist-info


#pip install 'html5<0.99'
pip install django-cms --upgrade
pip install djangocms-text-ckeditor --upgrade

./manage.py collectstatic --noinput

