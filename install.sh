#!/bin/bash
pip install pybind11==2.2.4
pip install -r requirements.txt
curl https://eu.ftp.opendatasoft.com/bmoreau/data_dumps.zip -L -o data_dumps.zip
unzip -o data_dumps.zip
rm data_dumps.zip
rm -r __MACOSX/
if [ ! -f chatbot_app/local_settings.py ]
then
    touch chatbot_app/local_settings.py
    echo "SECRET_KEY = '<SECRET_KEY>'" >> chatbot_app/local_settings.py
fi
yarn