from django.conf.urls import url

from chat.views.conversation_api import get_class_question, get_property_question, get_property_class_question, get_greeting
from chat.views.conversation_api import get_instructions
from chat.views.conversation_api import get_error_lov_unavailable, get_error_no_confirmed_class, get_salutation
from chat.views.correspondance_api import get_rml_mapping, get_class, result_confirmed_correspondances
from chat.views.correspondance_api import result_awaiting_correspondances, result_denied_correspondances
from chat.views.correspondance_api import get_field_class_correspondance, get_field_property_correspondance
from chat.views.correspondance_api import saturate_mapping
from chat.views.chat import semantize, chatbot_form
from chat.views.root import api_root

url_api = [
    url(r'^api/(?P<dataset_id>[\w_@-]+)/conversation/question/class', get_class_question, name='get_class_question'),
    url(r'^api/(?P<dataset_id>[\w_@-]+)/conversation/question/property-class', get_property_class_question, name='get_property_class_question'),
    url(r'^api/(?P<dataset_id>[\w_@-]+)/conversation/question/property', get_property_question, name='get_property_question'),
    url(r'^api/(?P<dataset_id>[\w_@-]+)/conversation/greeting', get_greeting, name='get_greeting'),
    url(r'^api/(?P<dataset_id>[\w_@-]+)/conversation/instructions', get_instructions, name='get_instructions'),
    url(r'^api/(?P<dataset_id>[\w_@-]+)/conversation/error/lov-unavailable', get_error_lov_unavailable, name='get_error_lov_unavailable'),
    url(r'^api/(?P<dataset_id>[\w_@-]+)/conversation/error/no-classes', get_error_no_confirmed_class, name='get_error_no_confirmed_class'),
    url(r'^api/(?P<dataset_id>[\w_@-]+)/conversation/salutation', get_salutation, name='get_salutation'),
    url(r'^api/ner', get_class, name='get_class'),
    url(r'^api/saturate', saturate_mapping, name='saturate_mapping'),
    url(r'^api/(?P<dataset_id>[\w_@-]+)/correspondances/confirmed', result_confirmed_correspondances, name='post_result_confirmed_correspondances'),
    url(r'^api/(?P<dataset_id>[\w_@-]+)/correspondances/awaiting', result_awaiting_correspondances, name='post_result_awaiting_correspondances'),
    url(r'^api/(?P<dataset_id>[\w_@-]+)/correspondances/denied', result_denied_correspondances, name='post_result_denied_correspondances'),
    url(r'^api/(?P<dataset_id>[\w_@-]+)/correspondances/mapping', get_rml_mapping, name='post_then_get_rml_mapping'),
    url(r'^api/(?P<dataset_id>[\w_@-]+)/correspondances/field/class', get_field_class_correspondance, name='get_field_class_correspondance'),
    url(r'^api/(?P<dataset_id>[\w_@-]+)/correspondances/field/property', get_field_property_correspondance, name='get_field_property_correspondance'),
    url(r'^api', api_root, name='api_root')
]

url_chatbot = [
    url(r'^chatbot/(?P<dataset_id>[\w_@-]+)/?$', semantize, name='chatbot_semantize'),
    url(r'^chatbot', chatbot_form, name='chatbot_form')
]

url_root = [
    url(r'^$', chatbot_form, name='root_chatbot_form')
]

urlpatterns = url_api
urlpatterns += url_chatbot
urlpatterns += url_root
