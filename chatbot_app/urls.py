from django.urls import re_path

from chat.views.correspondance_api import (
    get_rml_mapping,
    get_class,
    result_confirmed_correspondances,
)
from chat.views.correspondance_api import (
    result_awaiting_correspondances,
    result_denied_correspondances,
)
from chat.views.correspondance_api import (
    get_field_class_correspondance,
    get_field_property_correspondance,
)
from chat.views.correspondance_api import (
    saturate_mapping,
    catalog_search,
    catalog_dataset_lookup,
    dataset_records,
)
from chat.views.root import api_root, index

url_api = [
    re_path(
        r"^api/catalog/datasets/(?P<dataset_id>[\w_@-]+)/?$",
        catalog_dataset_lookup,
        name="catalog_dataset_lookup",
    ),
    re_path(
        r"^api/records/datasets/(?P<dataset_id>[\w_@-]+)/?$",
        dataset_records,
        name="dataset_records",
    ),
    re_path(r"^api/ner", get_class, name="get_class"),
    re_path(r"^api/saturate", saturate_mapping, name="saturate_mapping"),
    re_path(r"^api/catalog", catalog_search, name="catalog"),
    re_path(
        r"^api/(?P<dataset_id>[\w_@-]+)/correspondances/confirmed",
        result_confirmed_correspondances,
        name="post_result_confirmed_correspondances",
    ),
    re_path(
        r"^api/(?P<dataset_id>[\w_@-]+)/correspondances/awaiting",
        result_awaiting_correspondances,
        name="post_result_awaiting_correspondances",
    ),
    re_path(
        r"^api/(?P<dataset_id>[\w_@-]+)/correspondances/denied",
        result_denied_correspondances,
        name="post_result_denied_correspondances",
    ),
    re_path(
        r"^api/(?P<dataset_id>[\w_@-]+)/correspondances/mapping",
        get_rml_mapping,
        name="post_then_get_rml_mapping",
    ),
    re_path(
        r"^api/(?P<dataset_id>[\w_@-]+)/correspondances/field/class",
        get_field_class_correspondance,
        name="get_field_class_correspondance",
    ),
    re_path(
        r"^api/(?P<dataset_id>[\w_@-]+)/correspondances/field/property",
        get_field_property_correspondance,
        name="get_field_property_correspondance",
    ),
    re_path(r"^api", api_root, name="api_root"),
]

url_root = [re_path(r"^$", index, name="index")]

urlpatterns = url_api
urlpatterns += url_root
