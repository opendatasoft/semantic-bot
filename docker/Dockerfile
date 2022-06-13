ARG NODE_VERSION=14
ARG PYTHON_VERSION=3
ARG DEBIAN_VERSION=buster

FROM python:3.9-slim-buster as base

ENV LANG=C.UTF-8
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apt-get -y update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    g++ \
    make \
    unzip

RUN python -m pip install -U pip setuptools wheel virtualenv

ENV VIRTUALENV=/opt/venv
RUN groupadd --gid 1000 semantic-bot && \
  adduser --gecos ',,,' --uid 1000 --gid 1000 --disabled-password semantic-bot && \
  mkdir -p ${VIRTUALENV} && chown 1000:1000 ${VIRTUALENV} && \
  chown semantic-bot:semantic-bot .

USER semantic-bot
RUN python -m virtualenv --system-site-packages ${VIRTUALENV}
ENV PATH="${VIRTUALENV}/bin:$PATH"


FROM node:${NODE_VERSION} as front-app

WORKDIR /usr/src

COPY package.json yarn.lock ./
RUN yarn install --pure-lock-file
RUN yarn global add jshint --prefix /usr/local

COPY assets ./assets/
COPY webpack.config.js webpack.watch.config.js ./
RUN yarn run build

FROM base as semantic-bot

WORKDIR /usr/src/app

# Copy source and built files
COPY --chown=1000:1000 requirements.txt ./

RUN pip install pybind11==2.2.4
RUN pip install -r requirements.txt

COPY --chown=1000:1000 --from=front-app /usr/local/bin /usr/local/bin
COPY --chown=1000:1000 --from=front-app /usr/local/share/.config/yarn/global/ /usr/local/share/.config/yarn/global/
COPY --chown=1000:1000 --from=front-app /usr/src/node_modules/ ./node_modules/
COPY --chown=1000:1000 --from=front-app /usr/src/assets/ ./assets
COPY --chown=1000:1000 --from=front-app /usr/src/webpack-stats.json ./webpack-stats.json
COPY --chown=1000:1000 chat/ ./chat/
COPY --chown=1000:1000 chatbot/ ./chatbot/
COPY --chown=1000:1000 chatbot_app/ ./chatbot_app/
COPY --chown=1000:1000 utils/ ./utils/
COPY --chown=1000:1000 exp/ ./exp/
COPY --chown=1000:1000 logs/ ./logs/
COPY --chown=1000:1000 manage.py ./

ENTRYPOINT ["python"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]