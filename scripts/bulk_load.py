"""
Bulk Loads all .ttl files in /data_dumps into elasticsearch.
"""
import os
import argparse

import utils.elasticsearch as ElasticSearch
import elasticsearch.helpers

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatbot_app.settings")
DUMP_DIR = '../data_dumps'

TYPE_INDEX = 'rdf_types'
LABEL_INDEX = 'rdfs_labels'

TYPE_MAPPING = {
    "settings": {
        "number_of_shards": 2,
        "number_of_replicas": 0,  # this can be set as 1 after load
        "refresh_interval": "1h"  # we won't load data regularly
    },
    "mappings": {
        "properties": {
            "resource": {
                "type": "text"  # e.g., <http://dbpedia.org/resource/Opendatasoft>
            },
            "class": {
                "type": "text"  # e.g., <http://dbpedia.org/ontology/Company>
            }
        }
    }
}
LABEL_MAPPING = {
    "settings": {
        "number_of_shards": 2,
        "number_of_replicas": 0,  # this can be set as 1 after load
        "refresh_interval": "1h"  # we won't load data regularly
    },
    "mappings": {
        "properties": {
            "resource": {
                "type": "text"  # e.g., <http://dbpedia.org/resource/Opendatasoft>
            },
            "label": {
                "type": "text"  # e.g., Opendatasoft
            },
            "lang": {
                "type": "text"  # e.g., en
            }
        }
    }
}


def main():
    es_client = ElasticSearch.get_client()
    es_client.ping()
    load_data(es_client)


def load_data(es_client):
    # clean es indexes
    es_client.indices.delete(index=TYPE_INDEX, ignore=[400, 404])
    es_client.indices.delete(index=LABEL_INDEX, ignore=[400, 404])
    es_client.indices.create(index=TYPE_INDEX, body=TYPE_MAPPING)
    es_client.indices.create(index=LABEL_INDEX, body=LABEL_MAPPING)
    # then load
    for success, info in elasticsearch.helpers.parallel_bulk(es_client, _bulk_load(), chunk_size=5000):
        if not success:
            print('A document failed:', info)


def _bulk_load():
    for file_name in os.listdir(DUMP_DIR):
        if file_name.endswith(".ttl"):
            print(file_name)
            with open(f'{DUMP_DIR}/{file_name}') as file:
                line = file.readline()
                while line:
                    triple = line.split()[:3]
                    doc_index, doc = _triple_to_doc(triple)
                    if doc_index and doc:
                        yield {
                            "_index": doc_index,
                            "_source": doc
                        }
                    line = file.readline()


def _triple_to_doc(triple):
    doc_index, doc = None, None
    if len(triple) == 3:
        s = triple[0].strip()
        p = triple[1].strip()
        o = triple[2].strip()
        if p in ['<http://www.w3.org/2000/01/rdf-schema#label>',
                 'rdfs:label',
                 '<http://www.w3.org/2000/01/rdf-schema#comment>'
                 'rdfs:comment',
                 '<http://www.w3.org/2004/02/skos/core#altLabel>',
                 'skos:altLabel',
                 '<http://www.w3.org/2004/02/skos/core#hiddenLabel>',
                 'skos:hiddenLabel',
                 '<http://www.w3.org/2004/02/skos/core#prefLabel>',
                 'skos:prefLabel']:
            doc_index = LABEL_INDEX
            resource = s
            label = o
            # by default, lang is en
            lang = 'en'
            # we remove the double quotes from labels
            label = label.replace('"', '')
            if '@' in o:
                # label has a lang tag e.g., France@fr
                splitted_label = o.split('@')
                label = splitted_label[0]
                lang = splitted_label[1]
            doc = {
                'resource': resource,
                'label': label,
                'lang': lang
            }
        elif p in ['<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>', 'rdf:type', 'a']:
            doc_index = TYPE_INDEX
            resource = s
            cl = o
            doc = {
                'resource': resource,
                'class': cl
            }
    return doc_index, doc


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Bulk load rdf:labels and rdf:type datasets into elasticsearch.')
    main()