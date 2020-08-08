#!/bin/bash

cp /etc/nginx/template.conf /tmp/template.conf && envsubst < /tmp/template.conf > /etc/nginx/conf.d/default.conf && exec nginx -g 'daemon off;'
