#!/bin/bash -ex

export CLOUDSDK_CORE_DISABLE_PROMPTS=1
export CLOUDSDK_PYTHON_SITEPACKAGES=1

GCLOUD=${SNAP_CACHE_DIR}/google-cloud-sdk/bin/gcloud

if [ ! -x ${GCLOUD} ]; then
    wget https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-91.0.1-linux-x86_64.tar.gz
    tar zxf google-cloud-sdk-91.0.1-linux-x86_64.tar.gz -C ${SNAP_CACHE_DIR}
    rm google-cloud-sdk-91.0.1-linux-x86_64.tar.gz
fi

${GCLOUD} --quiet components update
${GCLOUD} auth activate-service-account --key-file .gcloud-key

export MODULE_NAME=$1
export VERSION="$2"
export DATABASE_POSTFIX="$3"
export DATABASE_NAME="cfl_${DATABASE_POSTFIX}"
export CACHE_PREFIX="${MODULE_NAME}-${VERSION}-"

./manage.py migrate --noinput

envsubst <app.yaml.tmpl >app.yaml

${GCLOUD} preview app --quiet deploy app.yaml --project ${APP_ID} --version ${VERSION} --no-promote

# Test the site
./test.sh ${MODULE_NAME} ${VERSION}

# Promote
${GCLOUD} preview app modules set-default --project ${APP_ID} --version ${VERSION} ${MODULE_NAME}

# Test the site - again!
./test.sh ${MODULE_NAME} default
