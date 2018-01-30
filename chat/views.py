# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods

import json

import utils.ods_catalog_api as ODSCatalogApi
import utils.ods_dataset_api as ODSDatasetApi
import chatbot.semantic_engine as SemanticEngine


@require_http_methods(['GET'])
def semantize(request, dataset_id):
    return render(request, 'chatbot_semantize.html', {})


@require_http_methods(['GET'])
def get_correspondances(request, dataset_id):
    ods_dataset_metas = ODSCatalogApi.dataset_meta_request(dataset_id)
    ods_dataset_records = ODSDatasetApi.dataset_records_request(dataset_id, 3)['records']
    correspondances = SemanticEngine.init_correspondances_set(ods_dataset_metas, ods_dataset_records)
    response = HttpResponse(
        json.dumps(correspondances),
        content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    return response


@require_http_methods(['GET'])
def get_classes_correspondances(request, dataset_id):
    ods_dataset_records = ODSDatasetApi.dataset_records_request(dataset_id, 3)['records']
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
