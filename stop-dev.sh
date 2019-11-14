#!/bin/bash

kill -9 $(ps aux | grep "python manage.py runserver" | grep -v grep | awk '{print $2}')
kill -2 $(ps aux | grep "webpack.watch.config.js" | grep -v grep | awk '{print $2}')