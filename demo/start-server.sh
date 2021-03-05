#!/bin/bash

cd /semantic-bot
yarn run watch &
#/usr/bin/python3 manage.py migrate
#/usr/bin/python3 manage.py collectstatic
/usr/bin/python3 manage.py runserver 0.0.0.0:80 
#yarn run watch &
