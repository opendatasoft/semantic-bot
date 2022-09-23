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
    curl \
    libarchive-tools \
    uwsgi \
    uwsgi-plugin-python3 \
    gettext-base

RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

RUN python -m pip install -U pip setuptools wheel pybind11 virtualenv
ENV VIRTUALENV=/opt/venv
RUN mkdir -p ${VIRTUALENV} && python -m virtualenv --system-site-packages ${VIRTUALENV}
ENV PATH="${VIRTUALENV}/bin:$PATH"

FROM node:${NODE_VERSION} as front-app

WORKDIR /usr/src/app

COPY package.json yarn.lock ./
RUN yarn install --pure-lock-file

COPY assets ./assets/
COPY webpack.config.js ./
RUN yarn run build

FROM base as semantic-bot

WORKDIR /usr/src/app

RUN curl -L -O https://eu.ftp.opendatasoft.com/bmoreau/data_dumps.zip

# Copy source and built files
COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY --from=front-app /usr/local/bin /usr/local/bin
COPY --from=front-app /usr/src/app/assets/bundles ./assets/bundles
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
COPY docker/nginx.default /etc/nginx/nginx.template
COPY docker/uwsgi.ini ./uwsgi.ini

RUN chmod +x entrypoint.sh
RUN chown -R www-data:www-data /usr/src/app

RUN env SECRET_KEY="nOt-s0-s3cr3t-k3Y" python -m manage collectstatic --noinput

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
CMD ["_start_uwsgi_"]
