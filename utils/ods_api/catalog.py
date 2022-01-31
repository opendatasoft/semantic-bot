import requests

from utils import requester


def search_v2(domain_id, where='', search='', refine='', exclude='', rows=10, start=0, sort='explore.popularity_score',
              api_key=None):
    params = {'where': where,
              'search': search,
              'refine': refine,
              'exclude': exclude,
              'rows': rows,
              'start': start,
              'sort': sort,
              'apikey': api_key}
    request = requests.get(f"https://{domain_id}.opendatasoft.com/api/v2/catalog/datasets/",
                           params,
                           timeout=requester.get_timeout(),
                           headers=requester.create_ods_headers())
    request.raise_for_status()
    return request.json()


def lookup_v2(domain_id, dataset_id, api_key=None):
    return search_v2(domain_id, where=f"datasetid='{dataset_id}'", api_key=api_key)