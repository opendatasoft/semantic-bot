import sys
import json

from utils.lov_api import LovApi
from utils.ods_catalog_api import ODSCatalogApi
from utils.ods_dataset_api import ODSDatasetApi
from utils.natural_language_processor import NLProcessor


def search_candidate(candidate, dataset_title, dataset_fields):
    # Find correspondance for dataset title
    candidate["dataset_title"] = {}
    for noun in NLProcessor.extract_noun(dataset_title):
        lov_results = LovApi.vocabulary_request(noun)["results"]
        if lov_results:
            candidate["dataset_title"][noun] = lov_results[0]

    candidate["fields"] = {}
    for field in dataset_fields:
        lov_results = LovApi.term_request(field, term_type='property')["results"]
        if lov_results:
            candidate["fields"][field] = lov_results[0]


if len(sys.argv) > 1:
    dataset_id = sys.argv[1]
    # Retrieve data and metadatas from the dataset that will be used for Ontology matching.
    dataset = ODSCatalogApi.dataset_meta_request(dataset_id)
    dataset_title = dataset['metas']['title']
    dataset_fields = []
    for field in dataset['fields']:
        dataset_fields.append(field['label'])
    records = ODSDatasetApi.dataset_records_request(dataset_id, 10)['records']

    # Candidate correspondances to be confirmed by a user.
    candidate = {}
    search_candidate(candidate, dataset_title, dataset_fields)

    with open('result.json', 'w') as outfile:
        json.dump(candidate, outfile, indent=4)
    sys.exit()
else:
    print 'ontobot.py <dataset_id>'
    sys.exit()
