#!/bin/bash -ex

export CLOUDSDK_CORE_DISABLE_PROMPTS=1
export CLOUDSDK_PYTHON_SITEPACKAGES=1

GCLOUD=${SEMAPHORE_CACHE_DIR}/google-cloud-sdk/bin/gcloud

if [ ! -x ${GCLOUD} ]; then
    wget https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-159.0.0-linux-x86_64.tar.gz
    tar zxf google-cloud-sdk-159.0.0-linux-x86_64.tar.gz -C ${SEMAPHORE_CACHE_DIR}
    rm google-cloud-sdk-159.0.0-linux-x86_64.tar.gz
fi

${GCLOUD} --quiet components update
${GCLOUD} auth activate-service-account --key-file .gcloud-key

export MODULE_NAME=$1
export VERSION="$2"
export DATABASE_POSTFIX="$3"
export DATABASE_NAME="cfl_${DATABASE_POSTFIX}"
export CACHE_PREFIX="${MODULE_NAME}-${VERSION}-"

#./manage.py migrate --noinput

envsubst <app.yaml.tmpl >app.yaml

${GCLOUD} app --quiet deploy app.yaml --project ${APP_ID} --version ${VERSION} --no-promote
${GCLOUD} app --quiet deploy cron.yaml --project ${APP_ID} --version ${VERSION} --no-promote

# Deploy the correct kubernetes cluster.
python clusters_setup/deploy.py "${VERSION}"

# Test the site
./test.sh ${MODULE_NAME} ${VERSION}

# Promote
${GCLOUD} app services set-traffic --project ${APP_ID} --splits ${VERSION}=1 ${MODULE_NAME} --migrate

# Test the site - again!
./test.sh ${MODULE_NAME} default
