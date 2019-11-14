from django.conf.urls import url

from chat.views.correspondance_api import get_rml_mapping, get_class, result_confirmed_correspondances
from chat.views.correspondance_api import result_awaiting_correspondances, result_denied_correspondances
from chat.views.correspondance_api import get_field_class_correspondance, get_field_property_correspondance
from chat.views.correspondance_api import saturate_mapping, catalog_search, catalog_dataset_lookup, dataset_records
from chat.views.root import api_root, index

url_api = [
    url(r'^api/catalog/datasets/(?P<dataset_id>[\w_@-]+)/?$', catalog_dataset_lookup, name='catalog_dataset_lookup'),
    url(r'^api/records/datasets/(?P<dataset_id>[\w_@-]+)/?$', dataset_records, name='dataset_records'),
    url(r'^api/ner', get_class, name='get_class'),
    url(r'^api/saturate', saturate_mapping, name='saturate_mapping'),
    url(r'^api/catalog', catalog_search, name='catalog'),
    url(r'^api/(?P<dataset_id>[\w_@-]+)/correspondances/confirmed', result_confirmed_correspondances,
        name='post_result_confirmed_correspondances'),
    url(r'^api/(?P<dataset_id>[\w_@-]+)/correspondances/awaiting', result_awaiting_correspondances,
        name='post_result_awaiting_correspondances'),
    url(r'^api/(?P<dataset_id>[\w_@-]+)/correspondances/denied', result_denied_correspondances,
        name='post_result_denied_correspondances'),
    url(r'^api/(?P<dataset_id>[\w_@-]+)/correspondances/mapping', get_rml_mapping,
        name='post_then_get_rml_mapping'),
    url(r'^api/(?P<dataset_id>[\w_@-]+)/correspondances/field/class', get_field_class_correspondance,
        name='get_field_class_correspondance'),
    url(r'^api/(?P<dataset_id>[\w_@-]+)/correspondances/field/property', get_field_property_correspondance,
        name='get_field_property_correspondance'),
    url(r'^api', api_root, name='api_root')
]

url_root = [
    url(r'^$', index, name='index')
]

urlpatterns = url_api
urlpatterns += url_root
