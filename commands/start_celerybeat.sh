#!/bin/bash

rm /srv/project/celerybeat-schedule /srv/project/celerybeat.pid
celery -A settings beat --loglevel=info --workdir=/srv/project/src --schedule=/srv/project/celerybeat-schedule --pidfile=/srv/project/celerybeat.pid
