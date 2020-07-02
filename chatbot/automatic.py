import argparse
import os

from utils.ods_api.catalog import lookup_v2
from utils.ods_api.dataset import records_v2
from chatbot.semantic_engine import get_field_class, get_field_property, _get_uri_suffix
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatbot_app.settings")

ROWS_NUMBER = 10

def main(domain_id, dataset_id):
    semantize(domain_id, dataset_id, settings.DATA_API_KEY)


def semantize(domain_id, dataset_id, api_key):
    dataset = lookup_v2(domain_id, dataset_id, api_key)['dataset']
    fields = get_fields(dataset)
    language = dataset.get('metas', {}).get('default', {}).get('language', 'en')
    correspondances = {'classes': [], 'properties': []}
    entities_recognition(dataset_id, domain_id, correspondances, fields, api_key, language)
    properties_recognition()


def entities_recognition(dataset_id, domain_id, correspondances, fields, api_key, language):
    records = records_v2(domain_id, dataset_id, rows=ROWS_NUMBER, api_key=api_key)
    for name in fields:
        class_correspondance = get_field_class(records['records'], fields[name], language)
        if class_correspondance:
            correspondances['classes'].append(class_correspondance)
            fields[name]['class'] = class_correspondance['class']
            # the strings are used to match the corresponding class with domain of properties
            strings = set()
            strings.add(class_correspondance['description'])
            strings |= set([_get_uri_suffix(uri) for uri in class_correspondance['sub'] + class_correspondance['eq']])
            fields[name]['strings'] = list(strings)


def properties_recognition(correspondances, fields, language):
    get_field_property(fields, language)


def get_fields(dataset):
    fields = {}
    for field in dataset['fields']:
        field['class'] = None
        field['strings'] = []
        fields[field['name']] = field
    return fields


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A tool that federate ods datasets by a specific class.')
    parser.add_argument('-D', '-domain_id', type=str, help='The domain-id of the domain', required=True)
    parser.add_argument('-d', '-dataset_id', type=str, help='The domain-id of the domain', required=True)
    args = parser.parse_args()
    main(args.D, args.d, args.a)