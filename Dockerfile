FROM alpine:3.10
MAINTAINER Vyacheslav Tykhonov
RUN apk update && apk add  --no-cache freetype && apk add python3 && apk add python3-dev && apk add py3-pip
RUN apk --update add libxml2-dev libxslt-dev libffi-dev gcc musl-dev libgcc openssl-dev curl
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev
RUN apk add --update nodejs npm
RUN apk add bash gcc gfortran python python-dev py-pip build-base wget freetype-dev libpng-dev openblas-dev
RUN pip3 install --upgrade pip
RUN pip3 install cython
RUN pip3 install matplotlib
COPY . /semantic-bot
RUN pip3 install pybind11==2.2.4
WORKDIR /semantic-bot
RUN pip3 install -r requirements.txt
RUN apk add npm
RUN npm install -g yarn
ENV WORKDIR=/semantic-bot
RUN npm i
ENV DJANGO_SETTINGS_MODULE=chatbot_app.settings
ENV PYTHONPATH=$PYTHONPATH:$WORKDIR
ENV DATADIR=$WORKDIR/data_dumps
ENTRYPOINT ["bash"]
EXPOSE 8000
EXPOSE 8001
