from rdflib import RDF, RDFS, OWL, XSD
import utils.lov_ods_api as LOV
import yaml

YARRRML_KEYS = {
    'mappings': ['mappings', 'mapping'],
    'predicateobjects': ['predicateobjects', 'predicateobject', 'po'],
    'predicates': ['predicates', 'predicate', 'p'],
    'objects': ['objects', 'object', 'o'],
    'value': ['value', 'v']
}

PREFIXES = {
    'rdfs:': str(RDFS),
    'rdf:': str(RDF),
    'owl:': str(OWL),
    'xsd:': str(XSD)
}

# YARRRML Syntax: http://rml.io/yarrrml/spec/


def saturate(rml_mapping):
    saturated_mapping = {'mappings': {}, 'sources': rml_mapping['sources']}
    prefixes = parse_prefixes(rml_mapping)
    for mapping_key, mapping in get_keys(rml_mapping, YARRRML_KEYS['mappings']).items():
        saturated_mapping['mappings'][mapping_key] = {'subject': parse_term(mapping['subject'], prefixes),
                                                      'source': mapping['source'],
                                                      'predicateobjects': []}
        for predicate_object in get_keys(mapping, YARRRML_KEYS['predicateobjects']):
            predicate_object = uniformize_predicate_object(predicate_object)
            if predicate_object:
                predicate_object = saturate_predicate_object(predicate_object, prefixes)
                for predicate in predicate_object[0]:
                    for object in predicate_object[1]:
                        po = list()
                        po.append(predicate)
                        po.extend(object)
                        if po not in saturated_mapping['mappings'][mapping_key]['predicateobjects']:
                            saturated_mapping['mappings'][mapping_key]['predicateobjects'].append(po)
    return yaml.safe_dump(saturated_mapping, default_flow_style=None)


def saturate_predicate_object(predicate_object, prefixes):
    saturated_predicate_object = [[], []]
    is_class_saturation = False
    for predicate in predicate_object[0]:
        predicate = parse_term(predicate, prefixes)
        saturated_predicate_object[0].append(predicate)
        if predicate == 'a':
            is_class_saturation = True
            break
        else:
            saturated_predicate_object = property_saturation(saturated_predicate_object, predicate)
    for object in predicate_object[1]:
        saturated_object = []
        for term in object:
            saturated_object.append(parse_term(term, prefixes))
        saturated_predicate_object[1].append(saturated_object)
        if is_class_saturation:
            class_saturation(saturated_predicate_object, saturated_object)
    return saturated_predicate_object


def property_saturation(saturated_predicate_object, predicate):
    lov_results = LOV.lookup_uri(predicate, term_type='property')['records']
    if lov_results:
        lov_result = lov_results[0]['record']['fields']
        super_properties = lov_result.get('sub_properties')
        equivalent_properties = lov_result.get('equivalent_properties')
        if super_properties:
            for super_property in super_properties:
                    saturated_predicate_object[0].append(super_property)
        if equivalent_properties:
            for equivalent_property in equivalent_properties:
                    saturated_predicate_object[0].append(equivalent_property)
    return saturated_predicate_object


def class_saturation(saturated_predicate_object, object):
    class_uri = object[0]
    lov_results = LOV.lookup_uri(class_uri, term_type='class')['records']
    if lov_results:
        lov_result = lov_results[0]['record']['fields']
        super_classes = lov_result.get('sub_classes')
        equivalent_classes = lov_result.get('equivalent_classes')
        if super_classes:
            for super_class in super_classes:
                saturated_predicate_object[1].append([super_class])
        if equivalent_classes:
            for equivalent_class in equivalent_classes:
                saturated_predicate_object[1].append([equivalent_class])
    return saturated_predicate_object


def parse_prefixes(rml_mapping):
    prefixes = PREFIXES
    if 'prefixes' in rml_mapping:
        for prefix, uri in rml_mapping['prefixes'].items():
            if prefix not in prefixes:
                prefixes[prefix] = uri
    return prefixes


def parse_term(term, prefixes):
    if term == str(RDF.type):
        return 'a'
    uri_prefix = '{}:'.format(term.split(':', 1)[0])
    if uri_prefix in prefixes:
        term = term.replace(uri_prefix, prefixes[uri_prefix])
    return term


def uniformize_predicate_object(predicate_object):
    # returns the short uniform version:
    # [[predicate1, predicate2], [object1, object2]]
    # predicate -> URI
    # object -> [Term/URI, ?language, ?datatype]
    uniformized_predicate_object = []
    if isinstance(predicate_object, list):
        # Shorcut version using lists
        if len(predicate_object) > 1:
            if isinstance(predicate_object[0], list):
                # [[predicate1, predicate2], ...]
                uniformized_predicate_object.append(predicate_object[0])
            else:
                # [predicate1, ...]
                uniformized_predicate_object.append([predicate_object[0]])
            if isinstance(predicate_object[1], list):
                # [..., [object1, object2]]
                if predicate_object[1]:
                    if isinstance(predicate_object[1][0], list):
                        # [..., [[Term/URI, ?language, ?datatype], ...]]
                        uniformized_predicate_object.append(predicate_object[1])
                    else:
                        # [..., [Term/URI, ?language, ?datatype]]
                        obj = []
                        for element in predicate_object[1]:
                            obj.append(element)
                        uniformized_predicate_object.append([obj])
            else:
                # [..., Term/URI, ?language, ?datatype]
                obj = []
                for element in predicate_object[1:]:
                    obj.append(element)
                uniformized_predicate_object.append([obj])
    else:
        # Original version using dict
        predicates = get_keys(predicate_object, YARRRML_KEYS['predicates'])
        objects = get_keys(predicate_object, YARRRML_KEYS['objects'])
        if not predicates or not objects:
            return []
        if isinstance(predicates, list):
            uniformized_predicate_object.append(predicates)
        else:
            uniformized_predicate_object.append([predicates])
        if isinstance(objects, list):
            objs = []
            for obj in objects:
                if isinstance(obj, dict):
                    value = get_keys(obj, YARRRML_KEYS['value'] + YARRRML_KEYS['mappings'])
                    language = obj.get('language')
                    datatype = obj.get('datatype')
                    objs.append(value)
                    if language:
                        objs.append("{}~lang".format(language))
                    if datatype:
                        objs.append(datatype)
                else:
                    objs.append(obj)
            uniformized_predicate_object.append([objs])
        else:
            uniformized_predicate_object.append([objects])
    return uniformized_predicate_object


def get_keys(d, keys):
    # Get the value of the first key in keys that match a key in d
    for key in keys:
        if key in d:
            return d[key]
    return {}
