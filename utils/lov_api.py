import json

from urllib2 import urlopen, Request, HTTPError
from urllib import urlencode

SEARCH_VOCAB_URL = "http://lov.okfn.org/dataset/lov/api/v2/vocabulary/search"
SEARCH_TERM_URL = "http://lov.okfn.org/dataset/lov/api/v2/term/search"


class LovNotAvailable(Exception):
    pass


class QueryParameterMissing(Exception):
    pass


class LovApi(object):
    """This class implements the LOV API v2 request."""

    @staticmethod
    def vocabulary_request(query, lang=None):
        """Search a vocabulary based on its title or prefix."""
        if query:
            params = {'q': query}
            if lang:
                params['lang'] = lang
            parameters = "?%s" % urlencode(params)
            return LovApi._request("%s%s" % (SEARCH_VOCAB_URL, parameters))
        else:
            raise QueryParameterMissing

    @staticmethod
    def term_request(query, term_type='class'):
        """Search a specific term (class or property) of a vocabulary."""
        if query:
            params = {'q': query, 'type': term_type}
            parameters = "?%s" % urlencode(params)
            return LovApi._request("%s%s" % (SEARCH_TERM_URL, parameters))
        else:
            raise QueryParameterMissing

    @staticmethod
    def _request(url):
        request = Request(url)
        try:
            response = urlopen(request)
        except HTTPError:
            raise LovNotAvailable
        raw_data = response.read().decode('utf-8')
        data = json.loads(raw_data)
        return data
