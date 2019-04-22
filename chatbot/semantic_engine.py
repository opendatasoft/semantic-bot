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

# Default class
THING_CLASS_CORRESPONDANCE = {'uri': 'http://schema.org/Thing',
                              'class': 'Thing',
                              'description': 'something',
                              'sub': [],
                              'eq': []}


def get_field_class(ods_dataset_records, field_metas, language='en'):
    """
        Finds the correspondance between classes in ontologies and one field of the dataset

        Uses two approaches:
        First, try to search classe of instances in knowledge graphs (ex. OpenDataSoft -> Company)
        Else, uses field name as the class to search
        Then, find the corresponding class in ontologies using Linked Open Vocabularies (LOV)
    """
    field_name = field_metas['name']
    candidate_classes = []
    # Search for instances of the dataset in resources of knowledge graphs and retrieve class of the resource
    for record in ods_dataset_records:
        if field_name in record['record']['fields']:
            value = record['record']['fields'][field_name]
            if has_no_numbers(value):
                types = DBPediaNER.entity_types_request(value, language)
                if not types:
                    # DBPedia could not find any class for this field
                    types = YagoNER.entity_types_request(value, language)
                if types:
                    candidate_classes.extend(types)
    if candidate_classes:
        common_class = Counter(candidate_classes).most_common(1)[0][0]
        common_class = smart_str(common_class)
        class_correspondance = get_class_correspondance(common_class, language)
    else:
        # Use the field label as the class to search
        field_label = smart_str(field_metas['label'])
        field_label = enrich_field(field_metas['type'], field_label)
        class_correspondance = get_class_correspondance(field_label, language)
    if class_correspondance:
        class_correspondance['label'] = field_metas['label']
        class_correspondance['field_name'] = field_name
    return class_correspondance


def get_field_property(field_metas, language='en'):
    """
        Finds the correspondances between properties in ontologies and on field of the dataset

        Uses field name as the property to search for
        find the corresponding property in ontologies using Linked Open Vocabularies (LOV)
    """
    prop = smart_str(field_metas['label'])
    prop = enrich_field(field_metas['type'], prop)
    property_correspondance = get_property_correspondance(prop, language)
    if property_correspondance:
        property_correspondance['label'] = field_metas['label']
        property_correspondance['field_name'] = field_metas['name']
        property_correspondance['type'] = field_metas['type']
    return property_correspondance


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
        else:
            property_correspondance['domain'] = THING_CLASS_CORRESPONDANCE
    else:
        property_correspondance['domain'] = THING_CLASS_CORRESPONDANCE
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
