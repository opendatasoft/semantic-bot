from __future__ import unicode_literals

import simplejson as json
import logging

from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods

import chatbot.conversation_engine as ConversationEngine
from .api_errors import bad_format_correspondance


@require_http_methods(['GET'])
def get_greeting(request, dataset_id):
    logging.getLogger("results_logger").info("[{}] Starting semantization".format(dataset_id))
    message = {'text': ConversationEngine.greeting()}
    response = HttpResponse(
        json.dumps(message),
        content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    return response


@require_http_methods(['GET'])
def get_instructions(request, dataset_id):
    message = {'text': ConversationEngine.instructions()}
    response = HttpResponse(
        json.dumps(message),
        content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    return response


@require_http_methods(['GET'])
def get_salutation(request, dataset_id):
    message = {'text': ConversationEngine.salutation()}
    response = HttpResponse(
        json.dumps(message),
        content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    return response


@require_http_methods(['GET'])
def get_error_no_confirmed_class(request, dataset_id):
    logging.getLogger("results_logger").info("[{}] No correspondances found".format(dataset_id))
    message = {'text': ConversationEngine.error_no_confirmed_class()}
    response = HttpResponse(
        json.dumps(message),
        content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    return response


@require_http_methods(['GET'])
def get_error_lov_unavailable(request, dataset_id):
    message = {'text': ConversationEngine.error_lov_unavailable()}
    response = HttpResponse(
        json.dumps(message),
        content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    return response


@require_http_methods(['POST'])
def get_class_question(request, dataset_id):
    try:
        correspondance = json.loads(request.body)
        field_name = correspondance['label']
        uri = correspondance['uri']
        class_description = correspondance['description']
        message = {'text': ConversationEngine.class_question(field_name, class_description, uri)}
        response = HttpResponse(
            json.dumps(message),
            content_type='application/json')
        response['Access-Control-Allow-Origin'] = '*'
    except (ValueError, KeyError):
        response = bad_format_correspondance()
    return response


@require_http_methods(['POST'])
def get_property_question(request, dataset_id):
    try:
        correspondance = json.loads(request.body)
        field_name = correspondance['label']
        uri = correspondance['uri']
        predicate_description = correspondance['description']
        domain_uri = None
        domain_description = None
        if correspondance['domain']:
            domain_uri = correspondance['domain'].get('uri')
            domain_description = correspondance['domain'].get('description')
        message = {'text': ConversationEngine.property_question(field_name, predicate_description, uri, domain_uri, domain_description)}
        response = HttpResponse(
            json.dumps(message),
            content_type='application/json')
        response['Access-Control-Allow-Origin'] = '*'
    except (ValueError, KeyError):
        response = bad_format_correspondance()
    return response


@require_http_methods(['POST'])
def get_property_class_question(request, dataset_id):
    try:
        correspondance = json.loads(request.body)
        predicate_description = correspondance['description']
        domain_uri = None
        domain_description = None
        if correspondance['domain']:
            domain_uri = correspondance['domain'].get('uri')
            domain_description = correspondance['domain'].get('description')
        message = {'text': ConversationEngine.property_class_question(predicate_description, domain_uri, domain_description)}
        response = HttpResponse(
            json.dumps(message),
            content_type='application/json')
        response['Access-Control-Allow-Origin'] = '*'
    except (ValueError, KeyError):
        response = bad_format_correspondance()
    return response
