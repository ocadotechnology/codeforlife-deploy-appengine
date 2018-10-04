#!/bin/bash -ex

GCLOUD=$1
NODE_SA_NAME=$2

${GCLOUD} iam service-accounts create $NODE_SA_NAME \
  --display-name "Node Service Account"

export NODE_SA_EMAIL=`gcloud iam service-accounts list --format='value(email)' \
  --filter='displayName:Node Service Account'`
export PROJECT=`gcloud config get-value project`

${GCLOUD} projects add-iam-policy-binding $PROJECT \
  --member serviceAccount:$NODE_SA_EMAIL \
  --role roles/monitoring.metricWriter
${GCLOUD} projects add-iam-policy-binding $PROJECT \
  --member serviceAccount:$NODE_SA_EMAIL \
  --role roles/monitoring.viewer
${GCLOUD} projects add-iam-policy-binding $PROJECT \
  --member serviceAccount:$NODE_SA_EMAIL \
  --role roles/logging.logWriter
${GCLOUD} projects add-iam-policy-binding $PROJECT \
  --member serviceAccount:$NODE_SA_EMAIL \
  --role roles/storage.objectViewer
