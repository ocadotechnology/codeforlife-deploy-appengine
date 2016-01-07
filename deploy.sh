#!/bin/bash -ex
curl -O -s https://storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.27.zip
sudo unzip -qq google_appengine_1.9.27.zip -d /opt/
rm google_appengine_1.9.27.zip
export PATH=/opt/google_appengine:$PATH

export DATABASE_NAME=cfl_$1

./manage.py migrate --noinput -v 2

appcfg.py update --oauth2_access_token=$GAE_OAUTH_TOKEN \
    -E DATABASE_NAME:$DATABASE_NAME \
    -E DJANGO_SECRET:$DJANGO_SECRET \
    -E RECAPTCHA_PRIVATE_KEY:$RECAPTCHA_PRIVATE_KEY \
    -E RECAPTCHA_PUBLIC_KEY:$RECAPTCHA_PUBLIC_KEY \
    -E CACHE_PREFIX:$1- \
    -V $2 \
    app.yaml



