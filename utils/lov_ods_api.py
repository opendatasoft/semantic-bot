import requests

from django.conf import settings

import utils.requester as Requester

# documentation: https://help.opendatasoft.com/apis/ods-search-v2/#dataset
SEARCH_CLASS_URL = "https://data.opendatasoft.com/api/v2/catalog/datasets/linked-open-vocabularies-classes%40public/records"
SEARCH_PROPERTY_URL = "https://data.opendatasoft.com/api/v2/catalog/datasets/linked-open-vocabularies-properties%40public/records"

# we try to choose the most used vocabulary first
SORT = '-reused_by_datasets, -occurencies_in_datasets'
FIELD_CLASS_PRIORITY = ['uri', 'equivalent_classes', 'label', 'description', 'sub_classes']
FIELD_PROPERTY_PRIORITY = ['uri', 'equivalent_properties', 'label', 'description']
FIELD_FILTER = "{} like '{}'"
ROWS = 5


class QueryParameterMissing(Exception):
    pass


def term_request(query, term_type='class', language='en'):
    language_selection_query = "language = '{}' OR language = 'undefined'".format(language)
    if query:
        query = query.split()
        if term_type == 'class':
            filter_query = _build_filter_query(FIELD_CLASS_PRIORITY, query)
            url = SEARCH_CLASS_URL
        else:
            filter_query = _build_filter_query(FIELD_PROPERTY_PRIORITY, query)
            url = SEARCH_PROPERTY_URL
        query = "({}) AND ({})".format(filter_query, language_selection_query)
        params = {'where': query, 'sort': SORT, 'rows': ROWS, 'apikey': settings.DATA_API_KEY}
        request = requests.get(url, params, timeout=Requester.get_timeout(), headers=Requester.create_ods_headers())
        request.raise_for_status()
        return request.json()
    else:
        raise QueryParameterMissing


def _build_filter_query(field_priority, query):
    filter_query = None
    for field in field_priority:
        for value in query:
            if filter_query:
                filter_query = "{} OR {}".format(filter_query, FIELD_FILTER.format(field, value))
            else:
                filter_query = FIELD_FILTER.format(field, value)
    return filter_query
