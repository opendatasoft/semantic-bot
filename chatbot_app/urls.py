from django.conf.urls import url

from chat.views.conversation_api import get_class_question, get_property_question, get_property_class_question, get_greeting
from chat.views.conversation_api import get_instructions, get_positive_answer, get_neutral_answer, get_negative_answer, get_salutation
from chat.views.conversation_api import get_error_lov_unavailable, get_error_no_confirmed_class
from chat.views.correspondance_api import get_correspondances, get_classes_correspondances, get_properties_correspondances, get_rml_mapping
from chat.views.correspondance_api import get_class, result_confirmed_correspondances, result_awaiting_correspondances, result_denied_correspondances
from chat.views.chat import semantize, chatbot_form
from chat.views.root import api_root

url_api = [
    url(r'^api/conversation/question/class', get_class_question, name='get_class_question'),
    url(r'^api/conversation/question/property-class', get_property_class_question, name='get_property_class_question'),
    url(r'^api/conversation/question/property', get_property_question, name='get_property_question'),
    url(r'^api/conversation/greeting', get_greeting, name='get_greeting'),
    url(r'^api/conversation/instructions', get_instructions, name='get_instructions'),
    url(r'^api/conversation/answer/positive', get_positive_answer, name='get_positive_answer'),
    url(r'^api/conversation/answer/neutral', get_neutral_answer, name='get_neutral_answer'),
    url(r'^api/conversation/answer/negative', get_negative_answer, name='get_negative_answer'),
    url(r'^api/conversation/error/lov-unavailable', get_error_lov_unavailable, name='get_error_lov_unavailable'),
    url(r'^api/conversation/error/no-classes', get_error_no_confirmed_class, name='get_error_no_confirmed_class'),
    url(r'^api/conversation/salutation', get_salutation, name='get_salutation'),
    url(r'^api/ner', get_class, name='get_class'),
    url(r'^api/(?P<dataset_id>[\w_@-]+)/correspondances/classes', get_classes_correspondances, name='get_dataset_classes_correspondances'),
    url(r'^api/(?P<dataset_id>[\w_@-]+)/correspondances/properties', get_properties_correspondances, name='get_dataset_classes_correspondances'),
    url(r'^api/(?P<dataset_id>[\w_@-]+)/correspondances/confirmed', result_confirmed_correspondances, name='post_result_confirmed_correspondances'),
    url(r'^api/(?P<dataset_id>[\w_@-]+)/correspondances/awaiting', result_awaiting_correspondances, name='post_result_awaiting_correspondances'),
    url(r'^api/(?P<dataset_id>[\w_@-]+)/correspondances/denied', result_denied_correspondances, name='post_result_denied_correspondances'),
    url(r'^api/(?P<dataset_id>[\w_@-]+)/correspondances/mapping', get_rml_mapping, name='post_then_get_rml_mapping'),
    url(r'^api/(?P<dataset_id>[\w_@-]+)/correspondances', get_correspondances, name='get_dataset_correspondances'),
    url(r'^api', api_root, name='api_root')
]

url_chatbot = [
    url(r'^chatbot/(?P<dataset_id>[\w_@-]+)/?$', semantize, name='chatbot_semantize'),
    url(r'^chatbot', chatbot_form, name='chatbot_form')
]

url_root = [
    url(r'', chatbot_form, name='root_chatbot_form')
]

urlpatterns = url_api
urlpatterns += url_chatbot
urlpatterns += url_root
