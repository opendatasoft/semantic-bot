"""
Bulk Loads all .ttl files in /data_dumps into elasticsearch.
"""
import os
import argparse

import utils.elasticsearch as ElasticSearch

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatbot_app.settings")


def main():
    es_client = ElasticSearch.get_client()
    es_client.ping()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Bulk load rdf:labels and rdf:type datasets into elasticsearch.')
    main()