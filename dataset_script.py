import argparse

import utils.ods_catalog_api as ODSCatalogApi
from ontobot import stat_datasets


def main():
    parser = argparse.ArgumentParser(prog='script', description='Semantize multiple datasets from OpenDataSoft platform.')
    parser.add_argument('start', metavar='S', type=int, default=0, nargs='?',
                        help='the dataset index to start from')
    parser.add_argument('end', metavar='E', type=int, default=300, nargs='?',
                        help='the number of dataset to analyse')
    args = parser.parse_args()
    start = args.start
    end = args.end
    while start < end:
        cmp = 0
        datasets = ODSCatalogApi.datasets_meta_request(start)['datasets']
        for dataset in datasets:
            dataset_id = dataset['datasetid']
            stat_datasets(dataset_id)
            cmp += 1
            print dataset_id
        start += cmp
        print start


if __name__ == "__main__":
    main()
