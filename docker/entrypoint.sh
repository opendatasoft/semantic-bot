#!/usr/bin/env bash

uwsgi --ini uwsgi.ini --master --pidfile=/tmp/project-master.pid --uid www-data --env DJANGO_SETTINGS_MODULE=chatbot_app.settings --daemonize=/var/log/uwsgi/semantic-bot.log
nginx -g "daemon off;"