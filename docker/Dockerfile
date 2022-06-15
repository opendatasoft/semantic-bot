ARG NODE_VERSION=15

FROM python:3.9-slim-bullseye as base

ENV LANG=C.UTF-8
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apt-get -y update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    g++ \
    make \
    unzip \
    nginx  \
    vim

RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

RUN python -m pip install -U pip setuptools wheel uwsgi

FROM node:${NODE_VERSION} as front-app

WORKDIR /usr/src/app

COPY package.json yarn.lock ./
RUN yarn install --pure-lock-file

COPY assets ./assets/
COPY webpack.config.js ./
RUN yarn run build

FROM base as semantic-bot

WORKDIR /usr/src/app

# Copy source and built files
COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY --from=front-app /usr/local/bin /usr/local/bin
COPY --from=front-app /usr/src/app/static/bundles ./assets/bundles
COPY --from=front-app /usr/src/app/assets/img ./assets/img
COPY --from=front-app /usr/src/app/webpack-stats.json ./webpack-stats.json
COPY chat/ ./chat/
COPY chatbot/ ./chatbot/
COPY chatbot_app/ ./chatbot_app/
COPY utils/ ./utils/
COPY exp/ ./exp/
COPY logs/ ./logs/
COPY manage.py ./
COPY docker/entrypoint.sh ./entrypoint.sh
COPY docker/nginx.default /etc/nginx/sites-available/default
COPY docker/uwsgi.ini ./uwsgi.ini

RUN python manage.py collectstatic
RUN chmod +x entrypoint.sh
RUN chown -R www-data:www-data /usr/src/app

RUN mkdir /var/log/uwsgi
RUN touch /var/log/uwsgi/semantic-bot.log
RUN chown -R www-data:www-data /var/log/uwsgi

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]