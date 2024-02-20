#!/bin/sh

set -e

CONF_TEMPLATE="/etc/nginx/default.conf.tpl"
CONF_FILE="/etc/nginx/default.conf"

envsubst < "${CONF_TEMPLATE}" > "${CONF_FILE}"
nginx -g 'daemon off;'