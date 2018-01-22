from rdflib import Dataset, Namespace, Literal, URIRef, BNode

rr = Namespace("http://www.w3.org/ns/r2rml#")
rml = Namespace("http://semweb.mmlab.be/ns/rml#")
ql = Namespace('http://semweb.mmlab.be/ns/ql#')


SUBJECT_URI = "uri_dataset/{class_name}/{{field_name}}"
SOURCE = "JSON DATASET URL"


def serialize(confirmed_correspondances):
    rdf_mapping = Dataset()
    rdf_mapping.bind("ql", ql)
    rdf_mapping.bind("rr", rr)
    rdf_mapping.bind("rml", rml)
    for field_name, class_correspondance in confirmed_correspondances['classes'].iteritems():
        add_class_map(rdf_mapping, class_correspondance, field_name)
    for field_name, property_correspondance in confirmed_correspondances['properties'].iteritems():
        add_predicate_map(rdf_mapping, property_correspondance, confirmed_correspondances['classes'], field_name)
    return rdf_mapping.serialize(format='trig')


def add_class_map(rdf_mapping, class_correspondance, field_name):
    map_id = URIRef("#{}".format(class_correspondance['class']))
    logical_source = rml['logicalSource']
    rdf_mapping.add((logical_source, rml['source'], Literal(SOURCE), map_id))
    rdf_mapping.add((logical_source, rml['referenceFormulation'], ql['JSONPath'], map_id))
    rdf_mapping.add((logical_source, rml['iterator'], Literal("$.[*].fields"), map_id))

    subject_map = rr['subjectMap']
    rdf_mapping.add((subject_map, rr['template'], Literal(SUBJECT_URI.format(class_name=class_correspondance['class'], field_name=field_name)), map_id))
    rdf_mapping.add((subject_map, rr['class'], URIRef(class_correspondance['uri']), map_id))


def add_predicate_map(rdf_mapping, property_correspondance, class_correspondances, field_name):
    map_id = URIRef("#{}".format(property_correspondance['associated_class']))
    predicate_map = rr['predicateObjectMap']
    rdf_mapping.add((predicate_map, rr['predicate'], URIRef(property_correspondance['uri']), map_id))
    object_node = BNode()
    if field_name in class_correspondances:
        parent_map_id = URIRef("#{}".format(class_correspondances[field_name]['class']))
        rdf_mapping.add((predicate_map, rr['objectMap'], object_node, map_id))
        rdf_mapping.add((object_node, rr['parentTriplesMap'], parent_map_id, map_id))
    else:
        rdf_mapping.add((predicate_map, rr['objectMap'], object_node, map_id))
        rdf_mapping.add((object_node, rml['reference'], Literal("$.{}".format(field_name)), map_id))
