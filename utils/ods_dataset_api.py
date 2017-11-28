import requests

import utils.requester as Requester

DATA_RECORD_API_URL = "https://data.opendatasoft.com/api/records/1.0/search/"


class DatasetIdMissing(Exception):
    pass


def dataset_records_request(dataset_id, rows=10):
    if dataset_id:
        params = {'dataset': dataset_id, 'rows': rows}
        request = requests.get(DATA_RECORD_API_URL, params, timeout=Requester.get_timeout())
        request.raise_for_status()
        return request.json()
    else:
        raise DatasetIdMissing
