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


def init_correspondances_set(ods_dataset_metas, ods_dataset_records):
    """
        Initialises the correspondances set object

        A correspondances (mappings, associations...) set is a python dict object containing:
        1. Correspondances between classes in ontologies and fields of a dataset
        2. Correspondances between properties in ontologies and fields of a dataset
    """
    language = get_dataset_language(ods_dataset_metas)
    candidate_correspondances = {'classes': get_dataset_classes(ods_dataset_records, ods_dataset_metas, language),
                                 'properties': get_dataset_properties(ods_dataset_metas)}
    return candidate_correspondances


def get_dataset_classes(ods_dataset_records, ods_dataset_metas, language='en'):
    """
        Initialises the correspondances between classes in ontologies and fields of the dataset

        Uses two approaches:
        First, try to search classe of instances in knowledge graphs (ex. OpenDataSoft -> Company)
        Else, uses field name as the class to search
        Then, find the corresponding class in ontologies using Linked Open Vocabularies
    """
    candidates_classes = {}
    # Search for instances of the dataset in resources of knowledge graphs and retrieve class of the resource
    for record in ods_dataset_records:
        for field, value in record['fields'].items():
            if has_no_numbers(value):
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
    # Use the field name as the class to search
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
    """
        Initialises the correspondances between properties in ontologies and fields of the dataset

        Uses field name as the property to search for
        find the corresponding property in ontologies using Linked Open Vocabularies (LOV)
    """
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


def get_class_correspondance(clss, language='en'):
    """
        Create a class correspondance object for the string 'clss'

        Searches for the class 'clss' in LOV
        Returns a class correspondances or None if not found or not good enough
        A class correspondance object is:
        - The URI of the class
        - The human readable description of the class
        - A list of class URI which the class is a sub-class of (Car -subClassOf-> Vehicle)
        - A list of properties URI that are equivalents to the class
    """
    lov_results = LovApi.term_request(clss, term_type='class', language=language)["records"]
    for lov_result in lov_results:
        lov_result = lov_result['record']
        if is_valid(lov_result):
            return _lov_to_class_correspondance(lov_result, clss)
    return None


def _lov_to_class_correspondance(lov_result, clss):
    """ Generate a class correspondance from a lov result """
    class_correspondance = {'uri': '', 'class': clss, 'description': clss, 'sub': [], 'eq': []}
    class_correspondance['uri'] = lov_result['fields']['uri']
    if lov_result['fields']['description'] and len(lov_result['fields']['description']) < 40:
        cleaned_description = BeautifulSoup(lov_result['fields']['description'], "html5lib").get_text().encode('utf8')
        class_correspondance['description'] = cleaned_description
    elif lov_result['fields']['label']:
        cleaned_description = BeautifulSoup(lov_result['fields']['label'], "html5lib").get_text().encode('utf8')
        class_correspondance['description'] = cleaned_description
    if lov_result['fields']['sub_classes']:
        class_correspondance['sub'] = lov_result['fields']['sub_classes']
    if lov_result['fields']['equivalent_classes']:
        class_correspondance['eq'] = lov_result['fields']['equivalent_classes']
    return class_correspondance


def get_property_correspondance(prop, language='en'):
    """
        Create a property correspondance object for the string 'prop'

        Searches for the property 'prop' in LOV
        Returns a property correspondances or None if not found or not good enough
        A property correspondance object is:
        - The URI of the property
        - The human readable description of the property
        - A list of properties URI which the property is a sub-property of (birthDate -subClassOf-> date)
        - A list of properties URI that are equivalents to the property
        - A domain that is a class correspondance
        - A range that is a class correspondance
    """
    lov_results = LovApi.term_request(prop, term_type='property', language=language)["records"]
    for lov_result in lov_results:
        lov_result = lov_result['record']
        if is_valid(lov_result):
            return _lov_to_property_correspondance(lov_result, prop, language)
    return None


def _lov_to_property_correspondance(lov_result, prop, language):
    """ Generate a property correspondance from a lov result """
    property_correspondance = {'uri': '', 'description': prop, 'sub': [], 'eq': [], 'domain': None, 'range': None}
    property_correspondance['uri'] = lov_result['fields']['uri']
    if lov_result['fields']['description'] and len(lov_result['fields']['description']) < 40:
        cleaned_description = BeautifulSoup(lov_result['fields']['description'], "html5lib").get_text().encode('utf8')
        property_correspondance['description'] = cleaned_description
    elif lov_result['fields']['label']:
        property_correspondance['description'] = lov_result['fields']['label']
    if lov_result['fields']['sub_properties']:
        property_correspondance['sub'] = lov_result['fields']['sub_properties']
    if lov_result['fields']['equivalent_properties']:
        property_correspondance['eq'] = lov_result['fields']['equivalent_properties']
    if lov_result['fields']['domain0']:
        domain_lov_results = LovApi.lookup_uri(uri=lov_result['fields']['domain0'],
                                               term_type='class',
                                               language=language)["records"]
        if domain_lov_results:
            domain_lov_result = domain_lov_results[0]['record']
            clss = _get_uri_suffix(lov_result['fields']['domain0'])
            property_correspondance['domain'] = _lov_to_class_correspondance(domain_lov_result, clss)
    if lov_result['fields']['range'] and 'http://www.w3.org/2001/XMLSchema#' not in lov_result['fields']['range']:
        # range is a class and not a XSD datatype
        domain_lov_results = LovApi.lookup_uri(uri=lov_result['fields']['range'],
                                               term_type='class',
                                               language=language)["records"]
        if domain_lov_results:
            domain_lov_result = domain_lov_results[0]['record']
            clss = _get_uri_suffix(lov_result['fields']['range'])
            property_correspondance['range'] = _lov_to_class_correspondance(domain_lov_result, clss)
    return property_correspondance


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


def has_no_numbers(value):
    """Checks if the string does not contains numbers"""
    if isinstance(value, str):
        return not(any(char.isdigit() for char in value))
    return False


def _get_uri_suffix(uri):
    """
        Returns the suffix (local name) of th uri

        :Example:

        >> _get_uri_suffix('http://example.org/test')
          'test'
        >> _get_uri_suffix('http://example.org/page#test2')
          'test2'
    """
    if '#' in uri:
        return uri.rsplit('#', 1)[-1]
    else:
        return uri.rsplit('/', 1)[-1]