#!/bin/bash
pip install pybind11==2.2.4
pip install -r requirements.txt
curl https://eu.ftp.opendatasoft.com/bmoreau/data-ner.zip -L -o data-ner.zip
unzip -o data-ner.zip -d /data-ner
rm data-ner.zip
rm -r __MACOSX/
if [ ! -f chatbot_app/local_settings.py ]
then
    touch chatbot_app/local_settings.py
    echo "SECRET_KEY = '<SECRET_KEY>'" >> chatbot_app/local_settings.py
fi
yarn