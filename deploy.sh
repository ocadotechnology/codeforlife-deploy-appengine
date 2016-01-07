#!/bin/bash -ex

export CLOUDSDK_CORE_DISABLE_PROMPTS=1
if [ ! -d /var/go/google-cloud-sdk ]; then
    curl https://sdk.cloud.google.com | bash
fi
/var/go/google-cloud-sdk/bin/gcloud --quiet components update
/var/go/google-cloud-sdk/bin/gcloud auth activate-service-account --key-file .gcloud-key

export MODULE_NAME=$1
export DATABASE_NAME="cfl_${MODULE_NAME}"
export CACHE_PREFIX="${MODULE_NAME}-"
export VERSION="$2"

./manage.py migrate --noinput -v 2

envsubst <app.yaml.tmpl >app.yaml

/var/go/google-cloud-sdk/bin/gcloud preview app --quiet --verbosity info deploy app.yaml --project ${APP_ID} --version ${VERSION}

# Test the site
./test.sh ${MODULE_NAME} ${VERSION}

# Promote
/var/go/google-cloud-sdk/bin/gcloud preview app modules set-default --project ${APP_ID} --version ${VERSION} ${MODULE_NAME}
