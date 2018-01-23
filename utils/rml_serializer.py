from rdflib import Graph, Namespace, Literal, URIRef, BNode

rr = Namespace("http://www.w3.org/ns/r2rml#")
rml = Namespace("http://semweb.mmlab.be/ns/rml#")
ql = Namespace('http://semweb.mmlab.be/ns/ql#')


SUBJECT_URI = "http://ods.dataset.com/{class_name}/{{{field_name}}}"


def serialize(confirmed_correspondances, dataset_id):
    rdf_mapping = Graph()
    rdf_mapping.bind("ql", ql)
    rdf_mapping.bind("rr", rr)
    rdf_mapping.bind("rml", rml)
    for field_name, class_correspondance in confirmed_correspondances['classes'].iteritems():
        add_class_map(rdf_mapping, class_correspondance, field_name, dataset_id)
    for field_name, property_correspondance in confirmed_correspondances['properties'].iteritems():
        add_predicate_map(rdf_mapping, property_correspondance, confirmed_correspondances['classes'], field_name)
    return rdf_mapping.serialize(format='ttl')


def add_class_map(rdf_mapping, class_correspondance, field_name, dataset_id):
    subject_id = URIRef("#{}".format(class_correspondance['class']))
    logical_source = rml['logicalSource']
    logical_source_node = BNode()
    rdf_mapping.add((subject_id, logical_source, logical_source_node))
    rdf_mapping.add((logical_source_node, rml['source'], Literal(dataset_id)))
    rdf_mapping.add((logical_source_node, rml['referenceFormulation'], ql['JSONPath']))
    rdf_mapping.add((logical_source_node, rml['iterator'], Literal("$.[*].fields")))

    subject_map_node = BNode()
    subject_map = rr['subjectMap']
    rdf_mapping.add((subject_id, subject_map, subject_map_node))
    rdf_mapping.add((subject_map_node, rr['template'], Literal(SUBJECT_URI.format(class_name=class_correspondance['class'], field_name=field_name))))
    rdf_mapping.add((subject_map_node, rr['class'], URIRef(class_correspondance['uri'])))


def add_predicate_map(rdf_mapping, property_correspondance, class_correspondances, field_name):
    subject_id = URIRef("#{}".format(property_correspondance['associated_class']))
    predicate_map = rr['predicateObjectMap']
    node = BNode()
    rdf_mapping.add((subject_id, predicate_map, node))
    rdf_mapping.add((node, rr['predicate'], URIRef(property_correspondance['uri'])))
    object_node = BNode()
    rdf_mapping.add((node, rr['objectMap'], object_node))
    if field_name in class_correspondances:
        parent_map_id = URIRef("#{}".format(class_correspondances[field_name]['class']))
        if parent_map_id != subject_id:
            rdf_mapping.add((object_node, rr['parentTriplesMap'], parent_map_id))
            return
    rdf_mapping.add((object_node, rml['reference'], Literal("$.{}".format(field_name))))
