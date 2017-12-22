import argparse
import json

import utils.ods_catalog_api as ODSCatalogApi
import utils.ods_dataset_api as ODSDatasetApi
from chatbot.chatbot import ChatBot


def semantize_dataset(dataset_id):
    # Retrieve data and metadatas from the dataset that will be used for Ontology matching.
    ods_dataset_metas = ODSCatalogApi.dataset_meta_request(dataset_id)
    ods_dataset_records = ODSDatasetApi.dataset_records_request(dataset_id, 2)['records']
    chatbot = ChatBot(ods_dataset_metas, ods_dataset_records)
    chatbot.start()
    with open('results/chatbot_results.json', 'w') as outfile:
        json.dump(chatbot.confirmed_correspondances, outfile)


def main():
    parser = argparse.ArgumentParser(prog='ontobot', description='Semantize a dataset from OpenDataSoft platform.')
    parser.add_argument('dataset_id', metavar='Dataset', type=str, nargs='+',
                        help='the dataset id on data.opendatasoft to semantize')
    args = parser.parse_args()
    dataset_id = args.dataset_id[0]
    semantize_dataset(dataset_id)


if __name__ == "__main__":
    main()
