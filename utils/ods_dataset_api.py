import requests

from django.conf import settings

import utils.requester as Requester

DATA_RECORD_API_URL = "https://data.opendatasoft.com/api/records/1.0/search/"
DATA_RECORD_API_V2_URL = "https://data.opendatasoft.com/api/v2/catalog/datasets/{}/records"


class DatasetIdMissing(Exception):
    pass


def dataset_records_request(dataset_id, rows=10):
    if dataset_id:
        params = {'dataset': dataset_id, 'rows': rows, 'apikey': settings.DATA_API_KEY}
        request = requests.get(DATA_RECORD_API_URL, params, timeout=Requester.get_timeout(), headers=Requester.create_ods_headers())
        request.raise_for_status()
        return request.json()
    else:
        raise DatasetIdMissing


def dataset_records_V2_request(dataset_id, rows=10):
    if dataset_id:
        params = {'rows': rows, 'apikey': settings.DATA_API_KEY}
        request = requests.get(DATA_RECORD_API_V2_URL.format(dataset_id), params, timeout=Requester.get_timeout(), headers=Requester.create_ods_headers())
        request.raise_for_status()
        return request.json()
    else:
        raise DatasetIdMissing
