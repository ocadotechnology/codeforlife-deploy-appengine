#!/bin/bash -ex
curl https://sdk.cloud.google.com | CLOUDSDK_CORE_DISABLE_PROMPTS=1 bash
~/google-cloud-sdk/bin/gcloud auth activate-service-account --key-file .gcloud-key

export DATABASE_NAME="cfl_$1"
export CACHE_PREFIX="$1-"
export VERSION="$2"

./manage.py migrate --noinput -v 2

envsubst <app.yaml.tmpl >app.yaml

~/google-cloud-sdk/bin/gcloud preview app --quiet --verbosity info deploy app.yaml --project $APP_ID --version $VERSION
