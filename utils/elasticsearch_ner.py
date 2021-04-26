import utils.elasticsearch as ElasticSearch

TYPES_TO_IGNORE = ['Thing', 'Agent']

es_client = ElasticSearch.get_client()


def entity_types_request(query, language='en'):
    """
    returns a list of classes that according to the query string.
    e.g., query='Opendatasoft' returns ['Company']
    """
    if query:
        query = query.encode("utf-8")
        res = es_client.search(index=ElasticSearch.LABEL_INDEX, body={
            # only gets the top 1 score matching result
            'size': 1,
            'query': {
                'match': {
                    'label': query
                }
            }
        })
        if res and res.get('hits', {}).get('total', {}).get('value', None):
            # we retrieve the resource IRIs (e.g., <http://dbpedia.org/resource/Opendatasoft>) of the rdfs:label
            # e.g., resource: <http://dbpedia.org/resource/Opendatasoft> label: Opendatasoft
            resources = set()
            for hit in res.get('hits', {}).get('hits', []):
                resource = hit.get('_source', {}).get('resource', None)
                if resource:
                    resources.add(resource)
            for resource in resources:
                # for each resource we get its types (classes)
                # e.g., resource: <http://dbpedia.org/resource/Opendatasoft> class: Company
                res = es_client.search(index=ElasticSearch.TYPE_INDEX, body={
                    'query': {
                        'match_phrase': {
                            'resource': resource
                        }
                    }
                })
                if res and res.get('hits', {}).get('total', {}).get('value', None):
                    # each resource has several hierarchical classes
                    # e.g., "Company" is also an "Organisation", etc.
                    classes = []
                    for hit in res.get('hits', {}).get('hits', []):
                        cl = hit.get('_source', {}).get('class', None)
                        if cl:
                            # remove namespace, '<' and '>'
                            cl = get_uri_suffix(cl[1:-1])
                            if not is_ignored(cl):
                                classes.append(cl)
                    if classes:
                        return classes
    return None


def is_ignored(class_name):
    """
    Checks if class is human readable and if class is not too generic (e.g., "Thing")
    """
    for type_to_ignore in TYPES_TO_IGNORE:
        if type_to_ignore in class_name or hasNumbers(class_name):
            return True


def hasNumbers(value):
    if isinstance(value, str):
        return any(char.isdigit() for char in value)
    return True


def get_uri_suffix(uri):
    """
    retrieves the suffix of an IRI or URI
    e.g., uri:<http://dbpedia.org/ontology/Company> returns "Company"
    """
    if '#' in uri:
        return uri.rsplit('#', 1)[-1]
    else:
        return uri.rsplit('/', 1)[-1]
