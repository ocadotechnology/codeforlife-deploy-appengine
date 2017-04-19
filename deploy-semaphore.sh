#!/bin/bash -ex

export CLOUDSDK_CORE_DISABLE_PROMPTS=1
export CLOUDSDK_PYTHON_SITEPACKAGES=1

GCLOUD=$SEMAPHORE_CACHE_DIR/google-cloud-sdk/bin/gcloud
SQL_PROXY=cloud_sql_proxy

if [ ! -x ${GCLOUD} ]; then
    wget https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-91.0.1-linux-x86_64.tar.gz
    tar zxf google-cloud-sdk-91.0.1-linux-x86_64.tar.gz -C $SEMAPHORE_CACHE_DIR/
    rm google-cloud-sdk-91.0.1-linux-x86_64.tar.gz
fi

${GCLOUD} --quiet components update
#${GCLOUD} auth activate-service-account --key-file .gcloud-key

if [ ! -x ${SQL_PROXY} ]; then
    wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64
    mv cloud_sql_proxy.linux.amd64 cloud_sql_proxy
    chmod +x cloud_sql_proxy
fi

export MODULE_NAME=$1
export VERSION="$2"
export DATABASE_POSTFIX="$3"
export DATABASE_NAME="cfl_${DATABASE_POSTFIX}"
export CACHE_PREFIX="${MODULE_NAME}-${VERSION}-"

./cloud_sql_proxy -instances=$CLOUD_SQL_NAME=tcp:3306 -credential_file=.gcloud-key

./manage.py migrate --noinput

envsubst <app.yaml.tmpl >app.yaml

${GCLOUD} app --quiet deploy app.yaml --project ${APP_ID} --version ${VERSION} --no-promote
#${GCLOUD} app --quiet deploy cron.yaml --project ${APP_ID} --version ${VERSION} --no-promote

# Test the site
./test.sh ${MODULE_NAME} ${VERSION}

# Promote
${GCLOUD} app services set-traffic --project ${APP_ID} --splits ${VERSION}=1 ${MODULE_NAME} --migrate

# Test the site - again!
./test.sh ${MODULE_NAME} default
