# Deprecated Replaced by virtuoso_ner

from hdt import HDTDocument

SCHEMA_NAME = "http://schema.org/name"
WIKIDATA_TYPE = 'http://www.wikidata.org/prop/P31'
WIKIDATA_TYPE_STATEMENT = 'http://www.wikidata.org/prop/statement/P31'

TYPES_TO_IGNORE = ['Wikimedia disambiguation page', 'Album', 'album']

try:
    wikidata = HDTDocument("data_dumps/wikidata/wikidata-20170313-all-BETA.hdt")
except RuntimeError:
    raise RuntimeError("Wikidata dump not found: Put wikidata dump into data_dumps/wikidata/ folder")


def entity_types_request(query, language='en'):
    if query:
        query = query.encode("utf-8")
        query = '"{}"@{}'.format(query, language)
        classes = []
        (triples_matching_query, cardinality) = wikidata.search_triples("", SCHEMA_NAME, query)
        if triples_matching_query:
            triple = triples_matching_query.next()
            entity = triple[0]
            (triples_entity_wikitype, cardinality) = wikidata.search_triples(entity, WIKIDATA_TYPE, "")
            if triples_entity_wikitype:
                triple = triples_entity_wikitype.next()
                type_entity = triple[2]
                (triples_entity_class, cardinality) = wikidata.search_triples(type_entity, WIKIDATA_TYPE_STATEMENT, "")
                if triples_entity_class:
                    triple = triples_entity_class.next()
                    entity_class = triple[2]
                    (triples_class_name, cardinality) = wikidata.search_triples(entity_class, SCHEMA_NAME, "")
                    for triple in triples_class_name:
                        class_name = triple[2]
                        if '@en' in class_name and '@en-' not in class_name:
                            if not is_ignored(class_name):
                                classes.append(class_name.split('@')[0].replace('"', ''))
                                break
        if classes:
            return classes
    return None


def is_ignored(class_name):
    for type_to_ignore in TYPES_TO_IGNORE:
        if type_to_ignore in class_name:
            return True
