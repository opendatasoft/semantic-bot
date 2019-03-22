from collections import Counter
from bs4 import BeautifulSoup
import requests

from django.utils.encoding import smart_str
from django.conf import settings

import utils.lov_ods_api as LovApi
import utils.dbpedia_ner as DBPediaNER
import utils.yago_ner as YagoNER
import utils.requester as Requester
from requests.exceptions import ConnectionError


def hasNoNumbers(value):
    if isinstance(value, str):
        return not(any(char.isdigit() for char in value))
    return False


def init_correspondances_set(ods_dataset_metas, ods_dataset_records):
    language = get_dataset_language(ods_dataset_metas)
    candidate_correspondances = {'classes': get_dataset_classes(ods_dataset_records, ods_dataset_metas, language),
                                 'properties': get_dataset_properties(ods_dataset_metas)}
    return candidate_correspondances


def get_dataset_classes(ods_dataset_records, ods_dataset_metas, language='en'):
    candidates_classes = {}
    # Search classes using Named Entity Recognition on instances
    for record in ods_dataset_records:
        for field, value in record['fields'].items():
            if hasNoNumbers(value):
                types = DBPediaNER.entity_types_request(value, language)
                if not types:
                    # DBPedia could not find any class for this field
                    types = YagoNER.entity_types_request(value, language)
                if types:
                    if field in candidates_classes:
                        candidates_classes[field].extend(types)
                    else:
                        candidates_classes[field] = types
    correspondances = []
    for field, classes in candidates_classes.items():
        common_class = Counter(classes).most_common(1)[0][0]
        common_class = smart_str(common_class)
        class_correspondance = get_class_correspondance(common_class, language)
        if class_correspondance:
            field_meta = get_field_metas(ods_dataset_metas, field)
            class_correspondance['label'] = field
            if field_meta and field_meta['label']:
                class_correspondance['label'] = field_meta['label']
            class_correspondance['field_name'] = field
            correspondances.append(class_correspondance)
    # Search classes using field name
    for field in ods_dataset_metas['fields']:
        if field['name'] not in candidates_classes:
            field_name = smart_str(field['label'])
            field_name = enrich_field(field['type'], field_name)
            class_correspondance = get_class_correspondance(field_name, language)
            if class_correspondance:
                class_correspondance['label'] = field['label']
                class_correspondance['field_name'] = field['name']
                correspondances.append(class_correspondance)
    return correspondances


def get_dataset_properties(ods_dataset_metas, language='en'):
    properties = []
    for field in ods_dataset_metas['fields']:
        prop = smart_str(field['label'])
        prop = enrich_field(field['type'], prop)
        property_correspondance = get_property_correspondance(prop, language)
        if property_correspondance:
            property_correspondance['label'] = field['label']
            property_correspondance['field_name'] = field['name']
            property_correspondance['type'] = field['type']
            properties.append(property_correspondance)
    return properties


def get_property_correspondance(prop, language='en'):
    response = {'uri': '', 'description': prop, 'sub': [], 'eq': []}
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
                response['sub'] = lov_result['fields']['sub_properties']
            if lov_result['fields']['equivalent_properties']:
                response['eq'] = lov_result['fields']['equivalent_properties']
            return response
    return None


def get_class_correspondance(clss, language='en'):
    response = {'uri': '', 'class': clss, 'description': clss, 'sub': [], 'eq': []}
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
                response['sub'] = lov_result['fields']['sub_classes']
            if lov_result['fields']['equivalent_classes']:
                response['eq'] = lov_result['fields']['equivalent_classes']
            return response
    return None


def is_valid(lov_result):
    """
        Checks if a result from linked open vocabulary (class or property) is good enough to be used by the chatbot

        Conditions are:
        - URI is available (returns HTTP code 200) activated if CHECK_URI_AVAILABILITY is set to True in configuration
        - Chatbot score of the result is equal or higher to the MINIMAL_CHATBOT_SCORE defined in configuration
        configuration is in your chatbot_app.local_settings.
        chatbot score is computed in utils.lov_ods_api._chatbot_score function.
    """
    if settings.CHECK_URI_AVAILABILITY:
        try:
            if requests.get(lov_result['fields']['uri'], timeout=Requester.get_timeout()).status_code != 200:
                return False
        except (requests.Timeout, ConnectionError):
            return False
    if lov_result['chatbot_score'] < settings.MINIMAL_CHATBOT_SCORE:
        return False
    return True


def get_dataset_language(ods_dataset_metas):
    """Gets the ISO 639-1 language code of the dataset. Default is 'eng'"""
    if 'metas' in ods_dataset_metas:
        if 'language' in ods_dataset_metas['metas']:
            return ods_dataset_metas['metas']['language']
    return 'eng'


def get_field_metas(ods_dataset_metas, field_name):
    """Finds the field in the dataset metadata using the field name"""
    for field in ods_dataset_metas['fields']:
        if field['name'] == field_name:
            return field
    return None


def enrich_field(field_type, field):
    """
      Semantically enrich a field name with its type

      :Example:

      >> enrich_field('date', birth)
      'birth date'

      .. todo:: Generalizing the research of hyponyms using a lexical database such as wordnet
    """
    # use field type
    if field_type in ['datetime', 'date'] and 'date' not in field.lower():
        field = "{} date".format(field)
    elif 'geo' in field_type and 'geo' not in field:
        field = "{} geo".format(field)
    # use hyponyms
    for place_hyponym in ['city', 'region', 'province', 'country', 'ville']:
        if place_hyponym in field.lower() and 'place' not in field.lower():
            field = "{} place".format(field)
    return field
