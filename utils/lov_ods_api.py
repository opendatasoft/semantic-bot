import re

import requests
from fuzzywuzzy import fuzz

from django.conf import settings

import utils.requester as Requester

# documentation: https://help.opendatasoft.com/apis/ods-search-v2/#dataset
SEARCH_CLASS_URL = "https://data.opendatasoft.com/api/v2/catalog/datasets/linked-open-vocabularies-classes%40public/records"
SEARCH_PROPERTY_URL = "https://data.opendatasoft.com/api/v2/catalog/datasets/linked-open-vocabularies-properties%40public/records"

FIELD_CLASS_PRIORITY = ['uri_suffix', 'equivalent_classes_suffix', 'label', 'description']
FIELD_CLASS_WEIGHT = [5, 1, 2, 1]
FIELD_PROPERTY_PRIORITY = ['uri_suffix', 'equivalent_properties_suffix', 'label', 'description']
FIELD_PROPERTY_WEIGHT = [5, 1, 2, 1]
FIELD_FILTER = "{} like '{}'"
ROWS = 50

ONTOLOGIES = [
    'http://dbpedia.org/ontology/',
    'http://schema.org/',
    'http://www.w3.org/2006/vcard/ns#',
    'http://xmlns.com/foaf/0.1/'
]

first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


class QueryParameterMissing(Exception):
    pass


def term_request(query, term_type='class', language='en'):
    language_selection_query = "language = '{}' OR language = 'undefined' OR language = 'en'".format(language)
    if query:
        query = _clean(query)
        splited_query = query.split()
        if term_type == 'class':
            field_priority = FIELD_CLASS_PRIORITY
            field_weight = FIELD_CLASS_WEIGHT
            filter_query = _build_filter_query(FIELD_CLASS_PRIORITY, splited_query)
            url = SEARCH_CLASS_URL
        else:
            field_priority = FIELD_PROPERTY_PRIORITY
            field_weight = FIELD_PROPERTY_WEIGHT
            filter_query = _build_filter_query(FIELD_PROPERTY_PRIORITY, splited_query)
            url = SEARCH_PROPERTY_URL
        ontology_query = _build_ontology_query()
        where = "({}) {} AND ({})".format(filter_query, ontology_query, language_selection_query)
        params = {'where': where, 'rows': ROWS, 'apikey': settings.DATA_API_KEY}
        request = requests.get(url, params, timeout=Requester.get_timeout(), headers=Requester.create_ods_headers())
        request.raise_for_status()
        result_set = _chatbot_score(request.json(), field_priority, field_weight, query)
        return result_set
    else:
        raise QueryParameterMissing


def lookup_uri(uri, term_type='class', language='en'):
    language_selection_query = "language = '{}' OR language = 'undefined' OR language = 'en'".format(language)
    if uri:
        if term_type == 'class':
            url = SEARCH_CLASS_URL
        else:
            url = SEARCH_PROPERTY_URL
        where = "(uri = '{}') AND ({})".format(uri, language_selection_query)
        params = {'where': where, 'rows': ROWS, 'apikey': settings.DATA_API_KEY}
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


def _build_ontology_query():
    ontology_query = ''
    for ontology in ONTOLOGIES:
        if ontology_query:
            ontology_query = "{} OR uri_prefix = '{}'".format(ontology_query, ontology)
        else:
            ontology_query = "uri_prefix = '{}'".format(ontology)
    if ontology_query:
        return "AND ({})".format(ontology_query)
    return ontology_query


def _chatbot_score(result_set, field_priority, field_weight, query):
    for result in result_set['records']:
            score = 0
            for i, field in enumerate(field_priority):
                score += field_weight[i] * fuzz.token_sort_ratio(result['record']['fields'][field], query)
            result['record']['chatbot_score'] = score
    result_set['records'] = sorted(result_set['records'], key=lambda result: result['record']['chatbot_score'], reverse=True)
    return result_set


def _clean(str):
    # UnCamel, UnSnake ...
    s1 = first_cap_re.sub(r'\1_\2', str)
    s2 = all_cap_re.sub(r'\1_\2', s1).lower()
    # ' char reserved in odsql
    return s2.replace('_', ' ').replace('-', ' ').replace("'", "")
