import argparse
import json

import utils.lov_api as LovApi
import utils.ods_catalog_api as ODSCatalogApi
import utils.ods_dataset_api as ODSDatasetApi
import utils.dandelion_api as DandelionApi
import utils.natural_language_processor as NLProcessor


# A changer en regardant dans les types des fields ?
def hasNoNumbers(inputString):
    return not(any(char.isdigit() for char in inputString))


def search_candidate(candidate, dataset_title, dataset_fields, dataset_records):
    # Find correspondance for dataset title
    candidate["dataset_title"] = {}
    for noun in NLProcessor.extract_noun(dataset_title):
        lov_results = LovApi.term_request(noun, term_type='class')["results"]
        if lov_results:
            candidate["dataset_title"][noun] = lov_results[0]

    candidate["fields"] = {}
    for field in dataset_fields:
        lov_results = LovApi.term_request(field, term_type='property')["results"]
        if lov_results:
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
    args = parser.parse_args()
    dataset_id = args.dataset_id[0]
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

    with open('{}.json'.format(dataset_id), 'w') as outfile:
        json.dump(candidate, outfile, indent=4)


if __name__ == "__main__":
    main()
