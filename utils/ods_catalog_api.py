import requests

import utils.requester as Requester

DATA_CATALOG_API_URL = "https://data.opendatasoft.com/api/datasets/1.0/{}/"
DATA_CATALOG_API_SEARCH_URL = "https://data.opendatasoft.com/api/datasets/1.0/search/"


class DatasetIdMissing(Exception):
    pass


def dataset_meta_request(dataset_id):
    if dataset_id:
        request = requests.get(DATA_CATALOG_API_URL.format(dataset_id), timeout=Requester.get_timeout(), headers=Requester.create_ods_headers())
        request.raise_for_status()
        return request.json()
    else:
        raise DatasetIdMissing


def datasets_meta_request(start=0, rows=100):
    params = {'start': start, 'rows': rows}
    request = requests.get(DATA_CATALOG_API_SEARCH_URL, params, timeout=Requester.get_timeout(), headers=Requester.create_ods_headers())
    request.raise_for_status()
    return request.json()
