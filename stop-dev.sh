#!/bin/bash

kill -9 $(ps aux | awk '/manage.py runserver/ {print $2}')
kill -2 $(ps aux | awk '/webpack.watch.config.js/ {print $2}')