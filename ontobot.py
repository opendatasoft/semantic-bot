import argparse
import json
from requests.exceptions import HTTPError

import utils.lov_api as LovApi
import utils.ods_catalog_api as ODSCatalogApi
import utils.ods_dataset_api as ODSDatasetApi
import utils.dandelion_api as DandelionApi
import utils.natural_language_processor as NLProcessor

LIMIT_SCORE_FIELD = 0.5000000
LIMIT_SCORE_TITLE = 0.5555555


# A changer en regardant dans les types des fields ?
def hasNoNumbers(value):
    if isinstance(value, unicode):
        return not(any(char.isdigit() for char in value))
    return False


def semantize_dataset(dataset_id):
    # Retrieve data and metadatas from the dataset that will be used for Ontology matching.
    dataset = ODSCatalogApi.dataset_meta_request(dataset_id)
    dataset_title = dataset['metas']['title']
    dataset_fields = []
    for field in dataset['fields']:
        dataset_fields.append(field['label'])
    records = ODSDatasetApi.dataset_records_request(dataset_id, 2)['records']
    # Candidate correspondances to be confirmed by a user.
    candidate = {}
    search_candidate(candidate, dataset_title, dataset_fields, records)

    with open('results/{}.json'.format(dataset_id), 'w') as outfile:
        json.dump(candidate, outfile, indent=4)


def stat_datasets(dataset_id):
    # First dataset (field_name with property)
    try:
        result = json.load(open('results/dataset1.json'))
    except IOError:
        result = {}
    dataset = ODSCatalogApi.dataset_meta_request(dataset_id)
    for field in dataset['fields']:
        field = field['name']
        record_id = "{}{}".format(dataset_id.encode('utf-8'), field.encode('utf-8'))
        if record_id not in result:
            lov_results = LovApi.term_request(field, term_type='property')["results"]
            if lov_results:
                if lov_results[0]['score'] > LIMIT_SCORE_FIELD:
                    result[record_id] = {}
                    result[record_id]['dataset_id'] = dataset_id
                    result[record_id]['field_name'] = field
                    result[record_id]['property'] = lov_results[0]['uri']
                    result[record_id]['score'] = lov_results[0]['score']
    with open('results/dataset1.json', 'w') as outfile:
        json.dump(result, outfile, indent=4)
    # Second dataset (dataset_id with field_name and class)
    try:
        result = json.load(open('results/dataset2.json'))
    except IOError:
        result = {}
    try:
        records = ODSDatasetApi.dataset_records_request(dataset_id, 2)['records']
    except HTTPError:
        return
    for record in records:
        for field, value in record['fields'].iteritems():
            if hasNoNumbers(value):
                types = DandelionApi.entity_types_request(value)
                if types:
                    for t in types:
                        record_id = "{}{}{}".format(dataset_id, field, t)
                        if record_id not in result:
                            result[record_id] = {}
                            result[record_id]['dataset_id'] = dataset_id
                            result[record_id]['field_name'] = field
                            result[record_id]['class'] = t
    with open('results/dataset2.json', 'w') as outfile:
        json.dump(result, outfile, indent=4)


def search_candidate(candidate, dataset_title, dataset_fields, dataset_records):
    # Find correspondance for dataset title
    candidate["dataset_title"] = {}
    for noun in NLProcessor.extract_noun(dataset_title):
        lov_results = LovApi.term_request(noun, term_type='class')["results"]
        if lov_results:
            if lov_results[0]['score'] > LIMIT_SCORE_TITLE:
                candidate["dataset_title"][noun] = lov_results[0]

    candidate["fields"] = {}
    for field in dataset_fields:
        lov_results = LovApi.term_request(field, term_type='property')["results"]
        if lov_results:
            if lov_results[0]['score'] > LIMIT_SCORE_FIELD:
                candidate["fields"][field] = lov_results[0]

    candidate["entities"] = {}
    for record in dataset_records:
        for field, value in record['fields'].iteritems():
            if hasNoNumbers(value):
                types = DandelionApi.entity_types_request(value)
                if types:
                    if field in candidate["entities"]:
                        candidate["entities"][field].extend(types)
                    else:
                        candidate["entities"][field] = types


def main():
    parser = argparse.ArgumentParser(prog='ontobot', description='Semantize a dataset from OpenDataSoft platform.')
    parser.add_argument('dataset_id', metavar='D', type=str, nargs='+',
                        help='the dataset id on data.opendatasoft')
    parser.add_argument('mod', metavar='M', type=int, choices=[0, 1], default=0, nargs='?',
                        help='The result file to be returned (default 0)')
    args = parser.parse_args()
    dataset_id = args.dataset_id[0]
    mod = args.mod
    if mod == 0:
        semantize_dataset(dataset_id)
    elif mod == 1:
        stat_datasets(dataset_id)


if __name__ == "__main__":
    main()
