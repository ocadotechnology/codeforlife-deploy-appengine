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
export DATABASE_HOST="/cloudsql/decent-digit-629:europe-west1:db"
export CACHE_PREFIX="${MODULE_NAME}-"
export GOOGLE_APPLICATION_CREDENTIALS=/home/runner/codeforlife-deploy-appengine/.gcloud-key

# Install the dependencies for the following deploy script.
# Kubernetes is a TEMPORARY solution. See issue 68.
pip install kubernetes
pip install pyyaml

# Authenticate the cluster by updating kubeconfig.
${GCLOUD} config set project ${APP_ID}
${GCLOUD} container clusters get-credentials aimmo-${MODULE_NAME} --zone europe-west1-b

# Deploy the correct kubernetes cluster.
python clusters_setup/deploy.py "${MODULE_NAME}"

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

${GCLOUD} app --quiet deploy app.yaml --project ${APP_ID} --version ${VERSION} --no-promote --no-cache
${GCLOUD} app --quiet deploy cron.yaml --project ${APP_ID} --version ${VERSION} --no-promote

# Test the site
./test.sh ${MODULE_NAME} ${VERSION}

# Promote
${GCLOUD} app services set-traffic --project ${APP_ID} --splits ${VERSION}=1 ${MODULE_NAME} --migrate

# Test the site - again!
./test.sh ${MODULE_NAME} default
