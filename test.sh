#!/bin/bash -ex

MODULE_NAME=$1
VERSION=$2

curl -I https://${VERSION}-dot-${MODULE_NAME}-dot-${APP_ID}.appspot.com/ | grep "HTTP/2 200"
