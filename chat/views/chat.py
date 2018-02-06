# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.http import require_http_methods


@require_http_methods(['GET'])
def semantize(request, dataset_id):
    return render(request, 'chatbot_semantize.html', {'dataset_id': dataset_id})
