from __future__ import unicode_literals


from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings

import simplejson as json
import logging
import yaml

import utils.elasticsearch_ner as ElasticSearchNer
import utils.yarrrml_saturator as YARRRMLSaturator
import utils.ods_catalog_api as ODSCatalog
import utils.ods_dataset_api as ODSRecords
import chatbot.semantic_engine as SemanticEngine
from .api_errors import bad_format_correspondance

if settings.MAPPING_SERIALIZER == 'YARRRML':
    import utils.yarrrml_serializer as MappingSerializer
else:
    import utils.rml_serializer as MappingSerializer

LOG_TEMPLATE_CLASS = '[{}] [Class] [{}] field:[{}] uri:[{}] field_type:[{}] field_is_facet:[{}]'
LOG_TEMPLATE_PROPERTY = '[{}] [Property] [{}] field_domain:[{}] class_domain[{}] -- uri:[{}] --> field_range:[{}] field_type:[{}] field_is_facet:[{}]'

@require_http_methods(['POST'])
def get_field_class_correspondance(request, dataset_id):
    try:
        json_body = json.loads(request.body)
        ods_dataset_records = json_body['records']
        fields = json_body['fields']
        field_name = request.GET.get('field', None)
        field_metas = fields[field_name]
        language = request.GET.get('lang', 'en')
        class_correspondance = SemanticEngine.get_field_class(ods_dataset_records, field_metas, language)
        response = HttpResponse(
            json.dumps(class_correspondance),
            content_type='application/json')
        response['Access-Control-Allow-Origin'] = '*'
    except (ValueError, KeyError):
        response = bad_format_correspondance()
    return response


@require_http_methods(['POST'])
def get_field_property_correspondance(request, dataset_id):
    try:
        json_body = json.loads(request.body)
        fields = json_body['fields']
        field_name = request.GET.get('field', None)
        field_metas = fields[field_name]
        language = request.GET.get('lang', 'en')
        property_correspondance = SemanticEngine.get_field_property(field_metas, language)
        response = HttpResponse(
            json.dumps(property_correspondance),
            content_type='application/json')
        response['Access-Control-Allow-Origin'] = '*'
    except (ValueError, KeyError):
        response = bad_format_correspondance()
    return response


@require_http_methods(['POST'])
def get_rml_mapping(request, dataset_id):
    try:
        confirmed_correspondances = json.loads(request.body)
        rml_mapping = MappingSerializer.serialize(confirmed_correspondances, dataset_id)
        response = HttpResponse(
            rml_mapping,
            content_type='text')
        response['Content-Disposition'] = 'attachment; filename="{}.yaml"'.format(dataset_id)
        response['Access-Control-Allow-Origin'] = '*'
        with open('results/{}.yaml'.format(dataset_id), 'w') as outfile:
            outfile.write(rml_mapping)
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
    classes = ElasticSearchNer.entity_types_request(term, lang)
    response = HttpResponse(
        json.dumps(classes),
        content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    return response


@require_http_methods(['GET'])
def catalog_search(request):
    search = request.GET.get('search', '')
    rows = request.GET.get('rows', 10)
    sort = request.GET.get('sort', 'explore.popularity_score')
    result = ODSCatalog.datasets_search_v2(search, rows, sort)
    response = HttpResponse(
        json.dumps(result),
        content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    return response


@require_http_methods(['GET'])
def catalog_dataset_lookup(request, dataset_id):
    result = ODSCatalog.dataset_meta_request(dataset_id)
    response = HttpResponse(
        json.dumps(result),
        content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    return response


@require_http_methods(['GET'])
def dataset_records(request, dataset_id):
    rows = request.GET.get('rows', settings.RECORD_NUMBER)
    result = ODSRecords.dataset_records_V2_request(dataset_id, rows)
    response = HttpResponse(
        json.dumps(result),
        content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    return response


@require_http_methods(['POST'])
def saturate_mapping(request):
    try:
        yarrrml_mapping = yaml.safe_load(request.body)
        yarrrml_mapping = YARRRMLSaturator.saturate(yarrrml_mapping)
        response = HttpResponse(
            yarrrml_mapping,
            content_type='text')
        response['Content-Disposition'] = 'attachment; filename="saturated_mapping.yaml"'
        response['Access-Control-Allow-Origin'] = '*'
    except (ValueError, KeyError):
        response = bad_format_correspondance()
    return response


def _correspondances_logger(dataset_id, correspondances, decision):
    fields_metas = correspondances['fields']
    for correspondance_class in correspondances.get('classes'):
        field_type = fields_metas.get(correspondance_class.get('field_name')).get('type')
        field_is_facet = False
        if fields_metas.get(correspondance_class.get('field_name')).get('annotations'):
            for annotation in fields_metas.get(correspondance_class.get('field_name')).get('annotations'):
                if 'facet' in annotation.get('name'):
                    field_is_facet = True
                    break
        logging.getLogger("results_logger").info(LOG_TEMPLATE_CLASS.format(dataset_id,
                                                                           decision,
                                                                           correspondance_class.get('field_name'),
                                                                           correspondance_class.get('uri'),
                                                                           field_type,
                                                                           field_is_facet))
    for correspondance_prop in correspondances.get('properties'):
        field_type = fields_metas.get(correspondance_prop.get('field_name')).get('type')
        field_is_facet = False
        if fields_metas.get(correspondance_prop.get('field_name')).get('annotations'):
            for annotation in fields_metas.get(correspondance_prop.get('field_name')).get('annotations'):
                if 'facet' in annotation.get('name'):
                    field_is_facet = True
                    break
        logging.getLogger("results_logger").info(LOG_TEMPLATE_PROPERTY.format(dataset_id,
                                                                              decision,
                                                                              correspondance_prop.get('associated_field'),
                                                                              correspondance_prop.get('associated_class'),
                                                                              correspondance_prop.get('uri'),
                                                                              correspondance_prop.get('field_name'),
                                                                              field_type,
                                                                              field_is_facet))
