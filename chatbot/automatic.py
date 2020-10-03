import argparse
import os

from utils.ods_api.catalog import lookup_v2
from utils.ods_api.dataset import records_v2
import utils.yarrrml_serializer as YARRRML
from chatbot.semantic_engine import get_field_class, get_field_property, _get_uri_suffix

from django.conf import settings
from rapidfuzz import fuzz

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatbot_app.settings")

ROWS_NUMBER = 10

TOO_GENERIC_CLASSES = ['http://schema.org/Thing',
                       'http://www.w3.org/2004/02/skos/core#Concept',
                       'http://www.w3.org/2002/07/owl#Thing']


def main(domain_id, dataset_id, output_file):
    yarrrml_mapping = semantize(domain_id, dataset_id, settings.DATA_API_KEY)
    output_file.write(yarrrml_mapping)
    output_file.close()


def semantize(domain_id, dataset_id, api_key):
    dataset = lookup_v2(domain_id, dataset_id, api_key)['dataset']
    fields = get_fields(dataset)
    language = dataset.get('metas', {}).get('default', {}).get('language', 'en')
    correspondances = {'classes': [], 'properties': []}
    entities_recognition(dataset_id, domain_id, correspondances, fields, api_key, language)
    properties_recognition(correspondances, fields, language)
    return YARRRML.serialize(correspondances, dataset_id)


def entities_recognition(dataset_id, domain_id, correspondances, fields, api_key, language):
    records = records_v2(domain_id, dataset_id, rows=ROWS_NUMBER, api_key=api_key)
    for name in fields:
        class_correspondance = get_field_class(records['records'], fields[name], language)
        if class_correspondance:
            correspondances['classes'].append(class_correspondance)
            update_field_class(fields, name, class_correspondance)


def update_field_class(fields, name, class_correspondance):
    fields[name]['class'] = class_correspondance['class']
    fields[name]['strings'] = get_strings(class_correspondance)


def get_strings(class_correspondance):
    # the strings are used to match the corresponding class with domain of properties
    strings = set()
    strings.add(class_correspondance['description'])
    strings |= set([_get_uri_suffix(uri) for uri in
                    class_correspondance['sub'] + class_correspondance['eq'] if
                    uri not in TOO_GENERIC_CLASSES])
    return strings


def properties_recognition(correspondances, fields, language):
    for name in fields:
        property_correspondance = get_field_property(fields[name], language)
        if property_correspondance:
            if property_correspondance['domain']:
                domain_field = find_field(property_correspondance['domain'], fields)
                if domain_field:
                    property_correspondance['associated_field'] = domain_field['name']
                    property_correspondance['associated_class'] = domain_field['class']
                    correspondances['properties'].append(property_correspondance)
            if property_correspondance['range'] and not fields[name]['class']:
                # the range of the property is a class and the field has not a class yet
                if property_correspondance['range']['uri'] not in TOO_GENERIC_CLASSES:
                    property_correspondance['range']['field_name'] = name
                    property_correspondance['range']['label'] = fields[name]['label']
                    correspondances['classes'].append(property_correspondance['range'])
                    update_field_class(fields, name, property_correspondance['range'])


def find_field(class_correspondance, fields):
    # finds the fields that best suits the class (often use to find the domain)
    class_strings = get_strings(class_correspondance)
    for name in fields:
        if fields[name]['strings']:
            field_class_strings = fields[name]['strings']
            for field_string in field_class_strings:
                for class_string in class_strings:
                    if fuzz.token_set_ratio(field_string, class_string, score_cutoff=90):
                        return fields[name]
    return None


def get_fields(dataset):
    fields = {}
    for field in dataset['fields']:
        field['class'] = None
        field['strings'] = []
        fields[field['name']] = field
    return fields


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A tool that automatically generates an RDF mapping for an Opendatasoft\'s dataset.')
    parser.add_argument('-D', '-domain_id', type=str, help='The domain-id of the domain', required=True)
    parser.add_argument('-d', '-dataset_id', type=str, help='The dataset-id of the dataset', required=True)
    parser.add_argument('-o', '-output', type=argparse.FileType('w'), help='the output file that will contain the mapping file',
                        required=True)
    args = parser.parse_args()
    main(args.D, args.d, args.o)
