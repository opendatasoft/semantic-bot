from hdt import HDTDocument

DBPEDIA_RESOURCE_URI = "http://dbpedia.org/resource/{resource_name}"
DBPEDIA_ONTOLOGY_URI = "http://dbpedia.org/ontology/"

try:
    eng_dbpedia = HDTDocument("dbpedia_dump/instance_type.hdt")
except RuntimeError:
    raise RuntimeError("DBpedia dump not found: Put dbpedia dump into dbpedia_dump folder")


def entity_types_request(query, lang='en'):
    query = query.encode("utf-8")
    query = query.title()
    query = query.replace(' ', '_')
    subject_query = DBPEDIA_RESOURCE_URI.format(resource_name=query)
    if lang == 'en':
        (triples, cardinality) = eng_dbpedia.search_triples(subject_query, "", "")
    else:
        (triples, cardinality) = eng_dbpedia.search_triples(subject_query, "", "")
    classes = []
    for triple in triples:
        cl = triple[2]
        if "owl#Thing" not in cl:
            cl = cl.replace(DBPEDIA_ONTOLOGY_URI, '')
            classes.append(cl)
    if classes:
        print classes
        return classes
    return None
