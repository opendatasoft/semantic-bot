from SPARQLWrapper import SPARQLWrapper, JSON
from fuzzywuzzy import fuzz

from django.conf import settings

TYPES_TO_IGNORE = ['Thing', 'Agent']
CHARS_TO_REMOVE = ['"', '\'', ',', '\n']


def entity_types_request(query, language='en'):
    sparql = SPARQLWrapper(f"http://127.0.0.1:{settings.VIRTUOSO_HTTP_SERVER_PORT}/sparql/")
    # Search for classes of resources with labels that contain the query string
    for char in CHARS_TO_REMOVE:
        query = query.replace(char, '')
    # full-text search words need at least 4 leading characters
    query_words = [term for term in query.split() if len(term) > 3]
    dict_results = {}
    cls = []
    if query_words:
        sparql.setQuery(f"""
        SELECT ?label ?class WHERE
        {{
         ?s ?p ?label .
         ?label bif:contains "'{' '.join(query_words)}'" .
         ?s a ?class .
        }}
        ORDER BY strlen(str(?label))
        LIMIT 1000
        """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        for result in results["results"]["bindings"]:
            label = result["label"]["value"]
            cl = get_uri_suffix(result["class"]["value"])
            if not is_ignored(cl):
                if label in dict_results:
                    dict_results[label]['classes'].add(cl)
                else:
                    dict_results[label] = {
                        'label': label,
                        'classes': {cl},
                        'score': fuzz.token_sort_ratio(label, query)
                    }
        ordered_results = sorted(dict_results.values(), key=lambda result: result['score'], reverse=True)
        if ordered_results:
            cls = list(ordered_results[0]['classes'])
    return cls


def is_ignored(class_name):
    for type_to_ignore in TYPES_TO_IGNORE:
        if type_to_ignore in class_name or has_numbers(class_name):
            return True


def has_numbers(value):
    if isinstance(value, str):
        return any(char.isdigit() for char in value)
    return True


def get_uri_suffix(uri):
    if '#' in uri:
        return uri.rsplit('#', 1)[-1].replace('wikicat_', '')
    else:
        return uri.rsplit('/', 1)[-1].replace('wikicat_', '')
