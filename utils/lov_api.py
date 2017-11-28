import requests

import utils.requester as Requester

SEARCH_VOCAB_URL = "http://lov.okfn.org/dataset/lov/api/v2/vocabulary/search"
SEARCH_TERM_URL = "http://lov.okfn.org/dataset/lov/api/v2/term/search"


class QueryParameterMissing(Exception):
    pass


def vocabulary_request(query, lang=None):
    if query:
        params = {'q': query}
        if lang:
            params['lang'] = lang
        request = requests.get(SEARCH_VOCAB_URL, params, timeout=Requester.get_timeout())
        request.raise_for_status()
        return request.json()
    else:
        raise QueryParameterMissing


def term_request(query, term_type='class'):
    if query:
        params = {'q': query, 'type': term_type}
        request = requests.get(SEARCH_TERM_URL, params, timeout=Requester.get_timeout())
        request.raise_for_status()
        return request.json()
    else:
        raise QueryParameterMissing
