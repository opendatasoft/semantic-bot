import argparse
import json

import utils.ods_catalog_api as ODSCatalogApi
import utils.ods_dataset_api as ODSDatasetApi
from chatbot.chatbot import ChatBot


def semantize_dataset(dataset_id):
    # Retrieve data and metadatas from the dataset that will be used for Ontology matching.
    ods_dataset_metas = ODSCatalogApi.dataset_meta_request(dataset_id)
    ods_dataset_records = ODSDatasetApi.dataset_records_request(dataset_id, 3)['records']
    try:
        with open('learned_denied_correspondances.json') as data_file:
            learned_denied_correspondances = json.load(data_file)
        chatbot = ChatBot(ods_dataset_metas, ods_dataset_records, learned_denied_correspondances)
    except IOError:
        chatbot = ChatBot(ods_dataset_metas, ods_dataset_records)
    chatbot.start()
    with open('learned_denied_correspondances.json', 'w') as outfile:
        json.dump(chatbot.learned_denied_correspondances, outfile)
    with open('results/chatbot_results.json', 'w') as outfile:
        json.dump(chatbot.candidate_correspondances, outfile)
        outfile.write("\n")
        json.dump(chatbot.confirmed_correspondances, outfile)
        outfile.write("\n")
        json.dump(chatbot.awaiting_correspondances, outfile)
        outfile.write("\n")
        json.dump(chatbot.denied_correspondances, outfile)


def main():
    parser = argparse.ArgumentParser(prog='ontobot', description='Semantize a dataset from OpenDataSoft platform.')
    parser.add_argument('dataset_id', metavar='Dataset', type=str, nargs='+',
                        help='the dataset id on data.opendatasoft to semantize')
    args = parser.parse_args()
    dataset_id = args.dataset_id[0]
    semantize_dataset(dataset_id)


if __name__ == "__main__":
    main()
