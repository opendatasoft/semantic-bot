from collections import Counter
from bs4 import BeautifulSoup
import requests
from django.utils.encoding import smart_str

import utils.lov_ods_api as LovApi
import utils.dbpedia_ner as DBPediaNER
import utils.yago_ner as YagoNER
import utils.requester as Requester
from requests.exceptions import ConnectionError

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
                if not types:
                    # DBPedia can't find a type for this field
                    types = YagoNER.entity_types_request(value, language)
                if types:
                    if field in candidates_classes:
                        candidates_classes[field].extend(types)
                    else:
                        candidates_classes[field] = types
    correspondances = []
    for field, classes in candidates_classes.iteritems():
        common_class = Counter(classes).most_common(1)[0][0]
        common_class = smart_str(common_class)
        class_correspondance = get_class_correspondance(common_class, language)
        if class_correspondance:
            field_meta = get_field(ods_dataset_metas, field)
            class_correspondance['label'] = field
            if field_meta and field_meta['label']:
                class_correspondance['label'] = field_meta['label']
            class_correspondance['field_name'] = field
            correspondances.append(class_correspondance)
    return correspondances


def get_dataset_properties(ods_dataset_metas, language='en'):
    properties = []
    for field in ods_dataset_metas['fields']:
        prop = smart_str(field['label'])
        if field['type'] in ['datetime', 'date']:
            prop = "{} date".format(prop)
        property_correspondance = get_property_correspondance(prop, language)
        if property_correspondance:
            property_correspondance['label'] = field['label']
            property_correspondance['field_name'] = field['name']
            property_correspondance['type'] = field['type']
            properties.append(property_correspondance)
    return properties


def get_property_correspondance(prop, language='en'):
    response = {'uri': '', 'description': prop, 'sub': []}
    lov_results = LovApi.term_request(prop, term_type='property', language=language)["records"]
    for lov_result in lov_results:
        lov_result = lov_result['record']
        if is_valid(lov_result):
            response['uri'] = lov_result['fields']['uri']
            if lov_result['fields']['description'] and len(lov_result['fields']['description']) < 40:
                cleaned_description = BeautifulSoup(lov_result['fields']['description'], "html5lib").get_text().encode('utf8')
                response['description'] = cleaned_description
            elif lov_result['fields']['label']:
                response['description'] = lov_result['fields']['label']
            if lov_result['fields']['sub_properties']:
                response['sub'] = eval(lov_result['fields']['sub_properties'])
            return response
    return None


def get_class_correspondance(clss, language='en'):
    response = {'uri': '', 'class': clss, 'description': clss, 'sub': []}
    lov_results = LovApi.term_request(clss, term_type='class', language=language)["records"]
    for lov_result in lov_results:
        lov_result = lov_result['record']
        if is_valid(lov_result):
            response['uri'] = lov_result['fields']['uri']
            if lov_result['fields']['description'] and len(lov_result['fields']['description']) < 40:
                cleaned_description = BeautifulSoup(lov_result['fields']['description'], "html5lib").get_text().encode('utf8')
                response['description'] = cleaned_description
            elif lov_result['fields']['label']:
                cleaned_description = BeautifulSoup(lov_result['fields']['label'], "html5lib").get_text().encode('utf8')
                response['description'] = cleaned_description
            if lov_result['fields']['sub_classes']:
                response['sub'] = eval(lov_result['fields']['sub_classes'])
            return response
    return None


def is_valid(lov_result):
    if CHECK_URI_AVAILABILITY:
        try:
            if requests.get(lov_result['fields']['uri'], timeout=Requester.get_timeout()).status_code != 200:
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
