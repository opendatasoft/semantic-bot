#!/usr/bin/env bash
set -e
# curl -L https://eu.ftp.opendatasoft.com/bmoreau/data_dumps.zip | bsdtar --exclude "__MACOSX*" --exclude "*.DS_Store" -tvf -

case "$*" in
    "_start_uwsgi_")
        bsdtar --exclude "__MACOSX*" --exclude "*.DS_Store" -xvf ./data_dumps.zip
        set -- uwsgi --ini uwsgi.ini --master --pidfile=/tmp/project-master.pid --uid www-data --env DJANGO_SETTINGS_MODULE=chatbot_app.settings
    ;;
    "_start_nginx_")
        shift
        if [ -n "${SEMANTIC_BOT_SVC}" ]
        then
            # shellcheck disable=SC2016 # because envsubst does needs unexpanded variable
            envsubst '${SEMANTIC_BOT_SVC}' < /etc/nginx/nginx.template > /etc/nginx/sites-available/default
        else
            echo "ERROR: Missing SEMANTIC_BOT_SVC environment variable!"
        fi
        set -- nginx -g 'daemon off; error_log /dev/stdout info;'
    ;;
    *)
        set -- "${@}"
    ;;
esac

exec "${@}"
