#!/bin/bash
pip install -r requirements.txt
docker-compose up -d
curl https://eu.ftp.opendatasoft.com/bmoreau/ttl_data_dumps.zip -L -o ttl_data_dumps.zip
unzip -o ttl_data_dumps.zip
rm ttl_data_dumps.zip
rm -r __MACOSX/
if [ ! -f chatbot_app/local_settings.py ]
then
    touch chatbot_app/local_settings.py
    echo "SECRET_KEY = '<SECRET_KEY>'" >> chatbot_app/local_settings.py
fi
python -m scripts.bulk_load
yarn