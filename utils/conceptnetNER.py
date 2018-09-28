import requests

CONCEPTNET_URL = "http://api.conceptnet.io/uri"

TYPES_TO_IGNORE = ['owl#Thing']


def entity_types_request(query, language='en'):
    if query:
        query = query.encode("utf-8")
        params = {'language': language, 'text': query}
        obj = requests.get(CONCEPTNET_URL.format(language=language, ressource_name=query), params=params).json()
    return None
