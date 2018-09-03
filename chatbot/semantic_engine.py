from collections import Counter
from bs4 import BeautifulSoup
import requests
from django.utils.encoding import smart_str

import utils.lov_api as LovApi
import utils.dbpedia_ner as DBPediaNER
# import utils.wikidata_ner as WikiDataNER
import utils.requester as Requester
from requests.exceptions import ConnectionError

LIMIT_SCORE_FIELD = 0.5000000
LIMIT_SCORE_CLASS = 0.5555555
CHECK_URI_AVAILABILITY = True


def hasNoNumbers(value):
    if isinstance(value, unicode):
        return not(any(char.isdigit() for char in value))
    return False


def init_correspondances_set(ods_dataset_metas, ods_dataset_records):
    language = get_dataset_language(ods_dataset_metas)
    candidate_correspondances = {'classes': get_dataset_classes(ods_dataset_records, ods_dataset_metas, language),
                                 'properties': get_dataset_properties(ods_dataset_metas)}
    return candidate_correspondances


def get_dataset_classes(ods_dataset_records, ods_dataset_metas, language='en'):
    candidates_classes = {}
    for record in ods_dataset_records:
        for field, value in record['fields'].iteritems():
            if hasNoNumbers(value):
                types = DBPediaNER.entity_types_request(value, language)
                # if not types:
                    # DBPedia can't find a type for this field
                    # types = WikiDataNER.entity_types_request(value, language)
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
            field_meta = get_field(ods_dataset_metas, field)
            class_correspondance['label'] = field
            if field_meta and field_meta['label']:
                class_correspondance['label'] = field_meta['label']
            class_correspondance['field_name'] = field
            correspondances.append(class_correspondance)
    return correspondances


def get_dataset_properties(ods_dataset_metas):
    properties = []
    for field in ods_dataset_metas['fields']:
        prop = field['label']
        if field['type'] in ['datetime', 'date']:
            prop = "{} date".format(smart_str(prop))
        property_correspondance = get_property_correspondance(prop)
        if property_correspondance:
            property_correspondance['label'] = field['label']
            property_correspondance['field_name'] = field['name']
            property_correspondance['type'] = field['type']
            properties.append(property_correspondance)
    return properties


def get_property_correspondance(prop):
    response = {'uri': '', 'description': ''}
    lov_results = LovApi.term_request(prop, term_type='property')["results"]
    for lov_result in lov_results:
        if is_valid(lov_result):
            response['uri'] = lov_result['uri'][0]
            if lov_result['highlight']:
                cleaned_description = BeautifulSoup(lov_result['highlight'][lov_result['highlight'].keys()[0]][0], "html5lib").get_text().encode('utf8')
                response['description'] = cleaned_description
            return response
    return None


def get_class_correspondance(clss):
    response = {'uri': '', 'class': clss, 'description': clss}
    lov_results = LovApi.term_request(clss, term_type='class')["results"]
    for lov_result in lov_results:
        if is_valid(lov_result):
            response['uri'] = lov_result['uri'][0]
            if lov_result['highlight']:
                cleaned_description = BeautifulSoup(lov_result['highlight'][lov_result['highlight'].keys()[0]][0], "html5lib").get_text().encode('utf8')
                response['description'] = cleaned_description
            return response
    return None


def is_valid(lov_result):
    if lov_result < LIMIT_SCORE_FIELD:
        return False
    if CHECK_URI_AVAILABILITY:
        try:
            if requests.get(lov_result['uri'][0], timeout=Requester.get_timeout()).status_code != 200:
                return False
        except (requests.Timeout, ConnectionError):
            return False
    return True


def get_dataset_language(ods_dataset_metas):
    if 'metas' in ods_dataset_metas:
        if 'language' in ods_dataset_metas['metas']:
            return ods_dataset_metas['metas']['language']
    return 'eng'


def get_field(ods_dataset_metas, field_name):
    for field in ods_dataset_metas['fields']:
        if field['name'] == field_name:
            return field
    return None
