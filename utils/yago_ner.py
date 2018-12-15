from hdt import HDTDocument

YAGO_RESOURCE_URI = "http://yago-knowledge.org/resource/{resource_name}"

TYPES_TO_IGNORE = ['owl#Thing', 'wikicat_ISO_basic_Latin_letters', 'wikicat_Latin_letters', 'wikicat_Vowel_letters']

try:
    yago = HDTDocument("data_dumps/yago/instance_type.hdt")
except RuntimeError:
    raise RuntimeError("YAGO dump not found: Put yago dump into data_dumps/yago/ folder")


def entity_types_request(query, language='en'):
    if query:
        query = query.encode("utf-8")
        query = to_yago_format(query)
        subject_query = YAGO_RESOURCE_URI.format(resource_name=query)
        (triples, cardinality) = yago.search_triples(subject_query, "", "")
        classes = []
        for triple in triples:
            cl = triple[2]
            if not is_ignored(cl):
                cl = cl.replace(YAGO_RESOURCE_URI.format(resource_name=''), '')
                cl = clean_yago_class(cl)
                classes.append(cl)
        if classes:
            return classes
    return None


def to_yago_format(query):
    query = query.title()
    query = query.replace(' ', '_')
    return query


def clean_yago_class(class_name):
    class_name = class_name.replace('_', ' ')
    class_name = class_name.replace('wikicat ', '')
    class_name = class_name.replace('wordnet ', '')
    return class_name


def is_ignored(class_name):
    for type_to_ignore in TYPES_TO_IGNORE:
        if type_to_ignore in class_name or not hasNoNumbers(class_name):
            return True


def hasNoNumbers(value):
    if isinstance(value, unicode):
        return not(any(char.isdigit() for char in value))
    return False
