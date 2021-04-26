import utils.elasticsearch as ElasticSearch

TYPES_TO_IGNORE = ['Thing', 'Agent']

es_client = ElasticSearch.get_client()


def entity_types_request(query, language='en'):
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
            # we retrieve the resources of the result
            resources = set()
            for hit in res.get('hits', {}).get('hits', []):
                resource = hit.get('_source', {}).get('resource', None)
                if resource:
                    resources.add(resource)
            for resource in resources:
                res = es_client.search(index=ElasticSearch.TYPE_INDEX, body={
                    # only gets the top 1 score matching result
                    'query': {
                        'match_phrase': {
                            'resource': resource
                        }
                    }
                })
                if res and res.get('hits', {}).get('total', {}).get('value', None):
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
    for type_to_ignore in TYPES_TO_IGNORE:
        if type_to_ignore in class_name or hasNumbers(class_name):
            return True


def hasNumbers(value):
    if isinstance(value, str):
        return any(char.isdigit() for char in value)
    return True


def get_uri_suffix(uri):
    if '#' in uri:
        return uri.rsplit('#', 1)[-1]
    else:
        return uri.rsplit('/', 1)[-1]
