import requests

import utils.requester as Requester

DATA_CATALOG_API_URL = "https://data.opendatasoft.com/api/datasets/1.0/{}/"


class DatasetIdMissing(Exception):
    pass


def dataset_meta_request(dataset_id):
    if dataset_id:
        request = requests.get(DATA_CATALOG_API_URL.format(dataset_id), timeout=Requester.get_timeout())
        request.raise_for_status()
        return request.json()
    else:
        raise DatasetIdMissing
