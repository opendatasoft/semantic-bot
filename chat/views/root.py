from __future__ import unicode_literals


from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from django.urls import get_resolver

import json


@require_http_methods(['GET'])
def api_root(request):
    patterns = get_patterns('api/')
    response = HttpResponse(
        json.dumps(patterns),
        content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    return response


@require_http_methods(['GET'])
def index(request):
    return render(request, 'index.html')


def get_patterns(root_path):
    resolver = get_resolver(None)
    patterns = sorted([
        (key, value[0][0][0])
        for key, value in resolver.reverse_dict.items()
        if isinstance(key, (str, bytes)) and (not(root_path) or root_path in value[0][0][0])
    ])
    return patterns
