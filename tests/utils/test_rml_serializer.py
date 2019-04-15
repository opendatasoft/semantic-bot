# -*- coding: utf-8 -*-
from utils import rml_serializer as RMLSerializer
from utils.rml_serializer import rr
from rdflib import Graph, URIRef


TEST_CORRESPONDANCES = {
  "classes": [{
    "eq": [],
    "sub": ["http://schema.org/Intangible"],
    "uri": "http://schema.org/BusTrip",
    "label": "Bus (ID)",
    "field_name": "idbus",
    "class": "Bus (ID)",
    "description": "A trip on a commercial bus line."
  }, {
    "eq": [],
    "sub": [],
    "uri": "http://schema.org/Thing",
    "label": "Bus (ID)",
    "field_name": "idbus",
    "class": "Thing",
    "description": "Something"
  }, {
    "eq": [],
    "sub": ["http://schema.org/MoveAction"],
    "uri": "http://schema.org/DepartAction",
    "label": "Depart",
    "field_name": "depart",
    "class": "Depart date",
    "description": "DepartAction"
  }, {
    "eq": [],
    "sub": ["http://www.w3.org/2006/vcard/ns#RelatedType"],
    "uri": "http://www.w3.org/2006/vcard/ns#Date",
    "label": "Arrivee",
    "field_name": "arrivee",
    "class": "Arrivee date",
    "description": "Date"
  }, {
    "eq": [],
    "sub": [],
    "uri": "http://schema.org/DateTime",
    "label": "Depart (theorique)",
    "field_name": "departtheorique",
    "class": "Depart (theorique) date",
    "description": "DateTime"
  }, {
    "eq": [],
    "sub": [],
    "uri": "http://schema.org/DateTime",
    "label": "Arrivee (theorique)",
    "field_name": "arriveetheorique",
    "class": "Arrivee (theorique) date",
    "description": "DateTime"
  }, {
    "eq": ["http://schema.org/Geo"],
    "sub": ["http://ontology.eil.utoronto.ca/icontact.owl#SchemaOrgThing", "http://rdfs.co/juso/Geometry", "http://schema.org/StructuredValue"],
    "uri": "http://schema.org/GeoCoordinates",
    "label": "Coordonnees",
    "field_name": "coordonnees",
    "class": "Coordonnees geo",
    "description": "GeoCoordinates"
  }, {
    "eq": [],
    "sub": ["http://dbpedia.org/ontology/PopulatedPlace"],
    "uri": "http://dbpedia.org/ontology/Settlement",
    "label": "Destination",
    "field_name": "destination",
    "class": "Settlement",
    "description": "settlement"
  }],
  "properties": [{
    "eq": [],
    "sub": [],
    "field_name": "numerobus",
    "uri": "http://schema.org/busNumber",
    "label": "Bus (numero)",
    "type": "int",
    "description": "The unique identifier for the bus.",
    "associated_class": "Bus (ID)",
    "associated_field": "idbus"
  }, {
    "eq": [],
    "sub": ["http://rdfs.co/juso/geometry"],
    "field_name": "coordonnees",
    "uri": "http://schema.org/geo",
    "label": "Coordonnees",
    "type": "geo_point_2d",
    "description": "The geo coordinates of the place.",
    "associated_class": "Depart (theorique) date",
    "associated_field": "departtheorique"
  }, {
    "eq": ["http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#participatesWith"],
    "sub": ["http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#coparticipatesWith"],
    "field_name": "destination",
    "uri": "http://dbpedia.org/ontology/destination",
    "label": "Destination",
    "type": "text",
    "description": "destination",
    "associated_class": "Bus (ID)",
    "associated_field": "idbus"
  }]
}


class TestRMLSerializer(object):

    def test_RML_mapping_classes(self):
        rdf_mapping = RMLSerializer.serialize(TEST_CORRESPONDANCES, 'dataset_test')
        rdf_mapping = Graph().parse(data=rdf_mapping, format="ttl")
        rdf_mapping_classes = []
        for class_triple in rdf_mapping.triples((None, rr['class'], None)):
            rdf_mapping_classes.append(class_triple[2])
        for class_correspondance in TEST_CORRESPONDANCES['classes']:
            assert URIRef(class_correspondance['uri']) in rdf_mapping_classes
            for sub_classe in class_correspondance['sub']:
                assert URIRef(sub_classe) in rdf_mapping_classes
            for eq_classe in class_correspondance['eq']:
                assert URIRef(eq_classe) in rdf_mapping_classes

    def test_RML_mapping_properties(self):
        rdf_mapping = RMLSerializer.serialize(TEST_CORRESPONDANCES, 'dataset_test')
        rdf_mapping = Graph().parse(data=rdf_mapping, format="ttl")
        rdf_mapping_properties = []
        for property_triple in rdf_mapping.triples((None, rr['predicate'], None)):
            rdf_mapping_properties.append(property_triple[2])
        for property_correspondance in TEST_CORRESPONDANCES['properties']:
            assert URIRef(property_correspondance['uri']) in rdf_mapping_properties
            for sub_property in property_correspondance['sub']:
                assert URIRef(sub_property) in rdf_mapping_properties
            for eq_property in property_correspondance['eq']:
                assert URIRef(eq_property) in rdf_mapping_properties
