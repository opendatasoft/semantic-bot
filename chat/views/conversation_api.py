from __future__ import unicode_literals


from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods

import simplejson as json

import chatbot.conversation_engine as ConversationEngine
from .api_errors import bad_format_correspondance


@require_http_methods(['GET'])
def get_greeting(request):
    message = {'text': ConversationEngine.greeting()}
    response = HttpResponse(
        json.dumps(message),
        content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    return response


@require_http_methods(['GET'])
def get_instructions(request):
    message = {'text': ConversationEngine.instructions()}
    response = HttpResponse(
        json.dumps(message),
        content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    return response


@require_http_methods(['GET'])
def get_positive_answer(request):
    message = {'text': ConversationEngine.reply_to_positive()}
    response = HttpResponse(
        json.dumps(message),
        content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    return response


@require_http_methods(['GET'])
def get_neutral_answer(request):
    message = {'text': ConversationEngine.reply_to_neutral()}
    response = HttpResponse(
        json.dumps(message),
        content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    return response


@require_http_methods(['GET'])
def get_negative_answer(request):
    message = {'text': ConversationEngine.reply_to_negative()}
    response = HttpResponse(
        json.dumps(message),
        content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    return response


@require_http_methods(['GET'])
def get_salutation(request):
    message = {'text': ConversationEngine.salutation()}
    response = HttpResponse(
        json.dumps(message),
        content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    return response


@require_http_methods(['GET'])
def get_error_no_confirmed_class(request):
    message = {'text': ConversationEngine.error_no_confirmed_class()}
    response = HttpResponse(
        json.dumps(message),
        content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    return response


@require_http_methods(['GET'])
def get_error_lov_unavailable(request):
    message = {'text': ConversationEngine.error_lov_unavailable()}
    response = HttpResponse(
        json.dumps(message),
        content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    return response


@require_http_methods(['POST'])
def get_class_question(request):
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
def get_property_question(request):
    try:
        correspondance = json.loads(request.body)
        field_name = correspondance['label']
        uri = correspondance['uri']
        predicate_description = correspondance['description']
        message = {'text': ConversationEngine.property_question(field_name, predicate_description, uri)}
        response = HttpResponse(
            json.dumps(message),
            content_type='application/json')
        response['Access-Control-Allow-Origin'] = '*'
    except (ValueError, KeyError):
        response = bad_format_correspondance()
    return response


@require_http_methods(['POST'])
def get_property_class_question(request):
    try:
        correspondance = json.loads(request.body)
        field_name = correspondance['label']
        uri = correspondance['uri']
        predicate_description = correspondance['description']
        message = {'text': ConversationEngine.property_class_question(field_name, predicate_description, uri)}
        response = HttpResponse(
            json.dumps(message),
            content_type='application/json')
        response['Access-Control-Allow-Origin'] = '*'
    except (ValueError, KeyError):
        response = bad_format_correspondance()
    return response
