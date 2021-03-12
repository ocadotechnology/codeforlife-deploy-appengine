#!/bin/bash -ex

export CLOUDSDK_CORE_DISABLE_PROMPTS=1
export CLOUDSDK_PYTHON_SITEPACKAGES=1

export MODULE_NAME=$1
export VERSION="$2"
export DATABASE_POSTFIX="$3"
export DATABASE_NAME="cfl_${DATABASE_POSTFIX}"
export CACHE_PREFIX="${MODULE_NAME}-"

# Install Cloud SQL Proxy
# TODO: move somewhere outside current dir
# wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy
# chmod +x cloud_sql_proxy

# Start Cloud SQL Proxy and migrate
# sudo ./cloud_sql_proxy -dir=/cloudsql &
# sleep 10
./manage.py migrate --no-input

if [ "$MODULE_NAME" = "default" ]
then
    export RECAPTCHA_PUBLIC_KEY=${RECAPTCHA_DEFAULT_PUBLIC_KEY} >/dev/null 2>&1
    export RECAPTCHA_PRIVATE_KEY=${RECAPTCHA_DEFAULT_PRIVATE_KEY} >/dev/null 2>&1
    export DOTMAILER_CREATE_CONTACT_URL=${DOTMAILER_CREATE_CONTACT_URL} >/dev/null 2>&1
    export DOTMAILER_ADDRESS_BOOK_URL=${DOTMAILER_ADDRESS_BOOK_URL} >/dev/null 2>&1
    export DOTMAILER_USER=${DOTMAILER_USER} >/dev/null 2>&1
    export DOTMAILER_PASSWORD=${DOTMAILER_PASSWORD} >/dev/null 2>&1
    export DOTMAILER_DEFAULT_PREFERENCES=${DOTMAILER_DEFAULT_PREFERENCES} >/dev/null 2>&1
else
    # dev will use staging key as well
    export RECAPTCHA_PUBLIC_KEY=${RECAPTCHA_STAGING_PUBLIC_KEY} >/dev/null 2>&1
    export RECAPTCHA_PRIVATE_KEY=${RECAPTCHA_STAGING_PRIVATE_KEY} >/dev/null 2>&1
    unset DOTMAILER_CREATE_CONTACT_URL >/dev/null 2>&1
    unset DOTMAILER_ADDRESS_BOOK_URL >/dev/null 2>&1
    unset DOTMAILER_USER >/dev/null 2>&1
    unset DOTMAILER_PASSWORD >/dev/null 2>&1
    unset DOTMAILER_DEFAULT_PREFERENCES >/dev/null 2>&1
fi

envsubst <django_site/kubeconfig.yaml.tmpl >django_site/kubeconfig.yaml
envsubst <app.yaml.tmpl >app.yaml

gcloud app --quiet deploy app.yaml --project ${APP_ID} --version ${VERSION} --no-promote --no-cache
gcloud app --quiet deploy cron.yaml --project ${APP_ID} --version ${VERSION} --no-promote

# Test the site
./test.sh ${MODULE_NAME} ${VERSION}

# Promote
gcloud app services set-traffic --project ${APP_ID} --splits ${VERSION}=1 ${MODULE_NAME} --migrate

# Test the site - again!
./test.sh ${MODULE_NAME} default
