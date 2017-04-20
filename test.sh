#!/bin/bash -ex

MODULE_NAME=$1
VERSION=$2

curl -v https://${VERSION}-dot-${MODULE_NAME}-dot-${APP_ID}.appspot.com/ -o /dev/null 2>&1
#| grep "200 OK"
