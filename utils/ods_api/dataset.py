import requests
import json

from utils import requester


def records_v2(domain_id, dataset_id, where='', search='', refine='', exclude='',  rows=10, start=0, sort='', select='',
               api_key=None):
    params = {'where': where,
              'search': search,
              'refine': refine,
              'exclude': exclude,
              'rows': rows,
              'start': start,
              'sort': sort,
              'select': select,
              'apikey': api_key}
    request = requests.get(f'https://{domain_id}.opendatasoft.com/api/v2/catalog/datasets/{dataset_id}/records',
                           params,
                           timeout=requester.get_timeout(),
                           headers=requester.create_ods_headers())
    request.raise_for_status()
    return request.json()


def export_records_v2(domain_id, dataset_id, where='', search='', rows=-1, start=0, sort='', select='', format='jsonl',
                      api_key=None):
    # Implemented for JSON line only (strongly advised for streaming operations)
    params = {'where': where,
              'search': search,
              'rows': rows,
              'start': start,
              'sort': sort,
              'select': select,
              'apikey': api_key}
    with requests.get(f'https://{domain_id}.opendatasoft.com/api/v2/catalog/datasets/{dataset_id}/exports/{format}',
                      params,
                      timeout=requester.get_timeout(),
                      headers=requester.create_ods_headers(),
                      stream=True) as request:
        request.raise_for_status()
        for line in request.iter_lines():
            if line:
                yield json.loads(line)
