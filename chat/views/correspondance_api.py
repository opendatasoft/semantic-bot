from __future__ import unicode_literals


from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods

import json
import logging

import utils.ods_catalog_api as ODSCatalogApi
import utils.ods_dataset_api as ODSDatasetApi
import utils.rml_serializer as RMLSerializer
import utils.dbpedia_ner as DBPediaNER
import chatbot.semantic_engine as SemanticEngine
from api_errors import bad_format_correspondance


@require_http_methods(['GET'])
def get_correspondances(request, dataset_id):
    logging.getLogger("results_logger").info("[{}] Starting semantization".format(dataset_id))
    ods_dataset_metas = ODSCatalogApi.dataset_meta_request(dataset_id)
    ods_dataset_records = ODSDatasetApi.dataset_records_request(dataset_id, 100)['records']
    correspondances = SemanticEngine.init_correspondances_set(ods_dataset_metas, ods_dataset_records)
    if not correspondances.get('classes'):
        logging.getLogger("results_logger").info("[{}] No correspondances found".format(dataset_id))
    logging.getLogger("results_logger").info("[{}] Starting semantization".format(dataset_id))
    response = HttpResponse(
        json.dumps(correspondances),
        content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    return response


@require_http_methods(['GET'])
def get_classes_correspondances(request, dataset_id):
    ods_dataset_records = ODSDatasetApi.dataset_records_request(dataset_id, 100)['records']
    correspondances = SemanticEngine.get_dataset_classes(ods_dataset_records)
    response = HttpResponse(
        json.dumps(correspondances),
        content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    return response


@require_http_methods(['GET'])
def get_properties_correspondances(request, dataset_id):
    ods_dataset_metas = ODSCatalogApi.dataset_meta_request(dataset_id)
    correspondances = SemanticEngine.get_dataset_properties(ods_dataset_metas)
    response = HttpResponse(
        json.dumps(correspondances),
        content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    return response


@require_http_methods(['POST'])
def get_rml_mapping(request, dataset_id):
    try:
        confirmed_correspondances = json.loads(request.body)
        rml_mapping = RMLSerializer.serialize(confirmed_correspondances, dataset_id)
        response = HttpResponse(
            rml_mapping,
            content_type='text/turtle')
        response['Content-Disposition'] = 'attachment; filename="{}.rml.ttl"'.format(dataset_id)
        response['Access-Control-Allow-Origin'] = '*'
        with open('results/{}.rml.ttl'.format(dataset_id), 'w') as outfile:
            outfile.write(rml_mapping)
        logging.getLogger("results_logger").info("[{}] semantization complete".format(dataset_id))
    except (ValueError, KeyError):
        response = bad_format_correspondance()
    return response


@require_http_methods(['POST'])
def result_confirmed_correspondances(request, dataset_id):
    try:
        confirmed_correspondances = json.loads(request.body)
        _correspondances_logger(dataset_id, confirmed_correspondances, 'CONFIRMED')
        response = HttpResponse(
            json.dumps(confirmed_correspondances),
            content_type='application/json')
        response['Access-Control-Allow-Origin'] = '*'
    except (ValueError, KeyError):
        response = bad_format_correspondance()
    return response


@require_http_methods(['POST'])
def result_awaiting_correspondances(request, dataset_id):
    try:
        awaiting_correspondances = json.loads(request.body)
        _correspondances_logger(dataset_id, awaiting_correspondances, 'PASSED')
        response = HttpResponse(
            json.dumps(awaiting_correspondances),
            content_type='application/json')
        response['Access-Control-Allow-Origin'] = '*'
    except (ValueError, KeyError):
        response = bad_format_correspondance()
    return response


@require_http_methods(['POST'])
def result_denied_correspondances(request, dataset_id):
    try:
        denied_correspondances = json.loads(request.body)
        _correspondances_logger(dataset_id, denied_correspondances, 'DENIED')
        response = HttpResponse(
            json.dumps(denied_correspondances),
            content_type='application/json')
        response['Access-Control-Allow-Origin'] = '*'
    except (ValueError, KeyError):
        response = bad_format_correspondance()
    return response


@require_http_methods(['GET'])
def get_class(request):
    term = request.GET.get('q', None)
    lang = request.GET.get('lang', 'en')
    classes = DBPediaNER.entity_types_request(term, lang)
    response = HttpResponse(
        json.dumps(classes),
        content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    return response


def _correspondances_logger(dataset_id, correspondances, decision):
    for correspondance_class in correspondances.get('classes'):
        logging.getLogger("results_logger").info("[{}] [Class] [{}] field:[{}] uri:[{}]".format(dataset_id,
                                                                                                decision,
                                                                                                correspondance_class.get('field_name'),
                                                                                                correspondance_class.get('uri')))
    for correspondance_prop in correspondances.get('properties'):
        logging.getLogger("results_logger").info("[{}] [Property] [{}] field_domain:[{}] class_domain[{}] -- uri:[{}] --> field_range:[{}]".format(dataset_id,
                                                                                                                                                   decision,
                                                                                                                                                   correspondance_prop.get('associated_field'),
                                                                                                                                                   correspondance_prop.get('associated_class'),
                                                                                                                                                   correspondance_prop.get('uri'),
                                                                                                                                                   correspondance_prop.get('field_name')))
