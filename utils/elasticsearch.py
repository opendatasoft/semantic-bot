import json

from elasticsearch import Elasticsearch

from chatbot_app.settings import ES_HOST, ES_PORT

try:
    es_client = Elasticsearch(f"{ES_HOST}:{ES_PORT}")
    print(json.dumps(Elasticsearch.info(es_client), indent=4 ), "\n")
except Exception as err:
    print("Elasticsearch() ERROR:", err, "\n")
    es_client = None


def get_client():
    return es_client
