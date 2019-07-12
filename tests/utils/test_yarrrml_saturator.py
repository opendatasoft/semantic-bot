# -*- coding: utf-8 -*-
from utils import yarrrml_saturator as YARRRMLSaturator
import yaml


YARRRML_MAPPING = '''
mappings:
  field-birth_cty:
    predicateobjects:
    - [a, 'http://schema.org/Place']
    - ['http://www.w3.org/2000/01/rdf-schema#label', $(birth_cty)]
    source: dataset-source
    subject: https://data.opendatasoft.com/ld/resources/roman-emperors@public/Place/$(birth_cty)
  field-birth_prv:
    predicateobjects:
    - [a, 'http://schema.org/Place']
    - ['http://www.w3.org/2000/01/rdf-schema#label', $(birth_prv)]
    source: dataset-source
    subject: https://data.opendatasoft.com/ld/resources/roman-emperors@public/Place/$(birth_prv)
  field-image:
    predicateobjects:
    - [a, 'http://dbpedia.org/ontology/Image']
    - ['http://www.w3.org/2000/01/rdf-schema#label', $(image)]
    source: dataset-source
    subject: https://data.opendatasoft.com/ld/resources/roman-emperors@public/Image/$(image)
  field-name:
    predicateobjects:
    - [a, 'http://schema.org/Person']
    - objects:
      - {mapping: field-image}
      predicates: http://schema.org/image
    - ['http://dbpedia.org/ontology/era', $(era)]
    - ['http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#isDescribedBy', $(era)]
    - ['http://dbpedia.org/ontology/dynasty', $(dynasty)]
    - ['http://dbpedia.org/ontology/notes', $(notes)]
    - ['http://xmlns.com/foaf/0.1/name', $(name)]
    - ['http://dbpedia.org/ontology/deathDate', $(death), 'http://www.w3.org/2001/XMLSchema#dateTime']
    - ['http://dbpedia.org/ontology/birthDate', $(birth), 'http://www.w3.org/2001/XMLSchema#dateTime']
    source: dataset-source
    subject: https://data.opendatasoft.com/ld/resources/roman-emperors@public/Person/$(name)
sources:
  dataset-source: [roman-emperors@public.json~jsonpath, '$.[*].fields']
'''


class TestYARRRMLSaturator(object):

    def test_mapping_saturation(self):
        rdf_mapping = yaml.safe_load(YARRRML_MAPPING)
        saturated_rdf_mapping = yaml.safe_load(YARRRMLSaturator.saturate(rdf_mapping))
        for mapping_key, mapping in rdf_mapping['mappings'].items():
            predicateobjects = mapping['predicateobjects']
            saturated_predicateobjects = saturated_rdf_mapping['mappings'][mapping_key]['predicateobjects']
            assert len(predicateobjects) <= len(saturated_predicateobjects)
