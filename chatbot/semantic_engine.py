from collections import Counter

import utils.lov_api as LovApi
import utils.dandelion_api as DandelionApi

LIMIT_SCORE_FIELD = 0.5000000
LIMIT_SCORE_CLASS = 0.5555555


def hasNoNumbers(value):
    if isinstance(value, unicode):
        return not(any(char.isdigit() for char in value))
    return False


def init_correspondances_set(ods_dataset_metas, ods_dataset_records):
    candidate_correspondances = {'classes': get_dataset_classes(ods_dataset_records),
                                 'properties': get_dataset_properties(ods_dataset_metas)}
    return candidate_correspondances


def get_dataset_classes(ods_dataset_records):
    candidates_classes = {}
    for record in ods_dataset_records:
        for field, value in record['fields'].iteritems():
            if hasNoNumbers(value):
                types = DandelionApi.entity_types_request(value)
                if types:
                    if field in candidates_classes:
                        candidates_classes[field].extend(types)
                    else:
                        candidates_classes[field] = types
    for field, classes in candidates_classes.iteritems():
        candidates_classes[field] = Counter(classes).most_common(1)[0][0]
    return candidates_classes


def get_dataset_properties(ods_dataset_metas):
    properties = {}
    for field in ods_dataset_metas['fields']:
        properties[field['name']] = field['label']
    return properties


def get_property_uri(prop):
    response = {'uri': '', 'description': ''}
    lov_results = LovApi.term_request(prop, term_type='property')["results"]
    if lov_results:
        if lov_results[0]['score'] > LIMIT_SCORE_FIELD:
            response['uri'] = lov_results[0]['uri']
            if lov_results[0]['highlight']:
                response['description'] = lov_results[0]['highlight'][lov_results[0]['highlight'].keys()[0]]
            return response
    return None


def get_class_uri(clss):
    response = {'uri': '', 'description': clss}
    lov_results = LovApi.term_request(clss, term_type='class')["results"]
    if lov_results:
        if lov_results[0]['score'] > LIMIT_SCORE_CLASS:
            response['uri'] = lov_results[0]['uri']
            if lov_results[0]['highlight']:
                response['description'] = lov_results[0]['highlight'][lov_results[0]['highlight'].keys()[0]]
            else:
                response['description'] = clss
            return response
    return None
