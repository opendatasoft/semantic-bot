from collections import Counter
from bs4 import BeautifulSoup

import utils.lov_api as LovApi
import utils.dbpedia_ner as DBPediaNER

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
                types = DBPediaNER.entity_types_request(value)
                if types:
                    if field in candidates_classes:
                        candidates_classes[field].extend(types)
                    else:
                        candidates_classes[field] = types
    correspondances = []
    for field, classes in candidates_classes.iteritems():
        common_class = Counter(classes).most_common(1)[0][0]
        class_correspondance = get_class_correspondance(common_class)
        if class_correspondance:
            class_correspondance['field_name'] = field
            correspondances.append(class_correspondance)
    return correspondances


def get_dataset_properties(ods_dataset_metas):
    properties = []
    for field in ods_dataset_metas['fields']:
        property_correspondance = get_property_correspondance(field['label'])
        if property_correspondance:
            property_correspondance['field_name'] = field['name']
            properties.append(property_correspondance)
    return properties


def get_property_correspondance(prop):
    response = {'uri': '', 'description': ''}
    lov_results = LovApi.term_request(prop, term_type='property')["results"]
    if lov_results:
        if lov_results[0]['score'] > LIMIT_SCORE_FIELD:
            response['uri'] = lov_results[0]['uri'][0]
            if lov_results[0]['highlight']:
                cleaned_description = BeautifulSoup(lov_results[0]['highlight'][lov_results[0]['highlight'].keys()[0]][0], "html5lib").get_text().encode('utf8')
                response['description'] = cleaned_description
            return response
    return None


def get_class_correspondance(clss):
    response = {'uri': '', 'class': clss, 'description': clss}
    lov_results = LovApi.term_request(clss, term_type='class')["results"]
    if lov_results:
        if lov_results[0]['score'] > LIMIT_SCORE_CLASS:
            response['uri'] = lov_results[0]['uri'][0]
            if lov_results[0]['highlight']:
                cleaned_description = BeautifulSoup(lov_results[0]['highlight'][lov_results[0]['highlight'].keys()[0]][0], "html5lib").get_text().encode('utf8')
                response['description'] = cleaned_description
            return response
    return None
