"""
Bulk Loads all .ttl files in /data_dumps into elasticsearch.
"""
import os
import argparse
from hashlib import sha1

import utils.elasticsearch as ElasticSearch
import elasticsearch.helpers

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatbot_app.settings")
DUMP_DIR = '../data_dumps'


def main():
    es_client = ElasticSearch.get_client()
    es_client.ping()
    for data in _bulk_load():
        print(data)


def _bulk_load(index='semantic_bot'):
    for file_name in os.listdir(DUMP_DIR):
        if file_name.endswith(".ttl"):
            print(file_name)
            with open(f'{DUMP_DIR}/{file_name}') as file:
                line = file.readline()
                while line:
                    triple = line.split()[:3]
                    doc_type, doc = zip(*_triple_to_doc(triple))
                    if doc_type and doc:
                        yield {
                            "_index": index,
                            "_type": doc_type,
                            "_id": sha1(line.encode('utf-8')).hexdigest(),
                            "_source": doc
                        }
                    line = file.readline()


def _triple_to_doc(triple):
    doc_type, doc = None, None
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
            doc_type = 'rdfs_labels'
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
            doc_type = 'rdf_types'
            resource = s
            cl = o
            doc = {
                'resource': resource,
                'class': cl
            }
    yield doc_type, doc


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Bulk load rdf:labels and rdf:type datasets into elasticsearch.')
    main()