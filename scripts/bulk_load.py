"""
Bulk Loads all .ttl files in /data_dumps into elasticsearch.
"""
import os
import argparse
import time

import utils.elasticsearch as ElasticSearch
import elasticsearch.helpers

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatbot_app.settings")
DUMP_DIR = os.path.join(os.path.dirname(__file__), '../data_dumps')


TYPE_MAPPING = {
    "settings": {
        "number_of_shards": 12,
        "number_of_replicas": 0,  # this can be set after load
        "refresh_interval": "-1"  # this can be set after load
    },
    "mappings": {
        "properties": {
            "resource": {
                "type": "text",  # e.g., <http://dbpedia.org/resource/Opendatasoft>
                "index_options": "docs"  # we don't want term frequencies to be indexed
            },
            "class": {
                "type": "text",  # e.g., <http://dbpedia.org/ontology/Company>
                "index_options": "docs"  # we don't want term frequencies to be indexed
            }
        }
    }
}
LABEL_MAPPING = {
    "settings": {
        "number_of_shards": 8,
        "number_of_replicas": 0,  # this can be set after load
        "refresh_interval": "-1"  # this can be set after load
    },
    "mappings": {
        "properties": {
            "resource": {
                "type": "text",  # e.g., <http://dbpedia.org/resource/Opendatasoft>
                "index_options": "docs"  # we don't want term frequencies to be indexed
            },
            "label": {
                "type": "text",  # e.g., Opendatasoft
                "index_options": "docs"  # we don't want term frequencies to be indexed
            },
            "lang": {
                "type": "text",  # e.g., en
                "index_options": "docs"  # we don't want term frequencies to be indexed
            }
        }
    }
}


def main():
    es_client = ElasticSearch.get_client()
    load_data(es_client)


def load_data(es_client):
    # clean es indexes
    es_client.indices.delete(index=ElasticSearch.TYPE_INDEX, ignore=[400, 404])
    es_client.indices.delete(index=ElasticSearch.LABEL_INDEX, ignore=[400, 404])
    es_client.indices.create(index=ElasticSearch.TYPE_INDEX, body=TYPE_MAPPING)
    es_client.indices.create(index=ElasticSearch.LABEL_INDEX, body=LABEL_MAPPING)
    # then load
    for success, info in elasticsearch.helpers.parallel_bulk(es_client, _bulk_load(), chunk_size=2000):
        if not success:
            print('A document failed:', info)
    es_client.indices.forcemerge(index='_all', max_num_segments=1, params={'request_timeout': 60 * 60 * 30})
    es_client.indices.refresh(index="_all")


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
            doc_index = ElasticSearch.LABEL_INDEX
            resource = s
            label = o
            # by default, lang is en
            lang = 'en'
            # we remove the double quotes from labels
            label = label.replace('"', '')
            if '@' in o:
                # label has a lang tag e.g., France@fr
                splitted_label = label.split('@')
                label = splitted_label[0]
                lang = splitted_label[1]
            doc = {
                'resource': resource,
                'label': label,
                'lang': lang
            }
        elif p in ['<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>', 'rdf:type', 'a']:
            doc_index = ElasticSearch.TYPE_INDEX
            resource = s
            cl = o
            doc = {
                'resource': resource,
                'class': cl
            }
    return doc_index, doc


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Bulk load rdf:labels and rdf:type datasets into elasticsearch.')
    start = time.time()
    main()
    end = time.time()
    print(f"Data loaded in: {end - start} seconds")