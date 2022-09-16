#!/usr/bin/env bash
set -e
# curl -L https://eu.ftp.opendatasoft.com/bmoreau/data_dumps.zip | bsdtar --exclude "__MACOSX*" --exclude "*.DS_Store" -tvf -

# uwsgi --ini uwsgi.ini --master --pidfile=/tmp/project-master.pid --uid www-data --env DJANGO_SETTINGS_MODULE=chatbot_app.settings
if [ "$*" != "" ]; then
    # If args are passed to the entrypoint, replace exec command with args
    set -- "${@}"
fi

exec "${@}"
