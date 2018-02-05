"""chatbot_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from chat.views.conversation_api import get_class_question, get_property_question, get_greeting, get_instructions
from chat.views.conversation_api import get_positive_answer, get_neutral_answer, get_negative_answer, get_salutation
from chat.views.correspondance_api import get_correspondances, get_classes_correspondances, get_properties_correspondances
from chat.views.chat import semantize

urlpatterns = [
    url(r'^api/conversation/question/class', get_class_question, name='get_class_question'),
    url(r'^api/conversation/question/property', get_property_question, name='get_property_question'),
    url(r'^api/conversation/greeting', get_greeting, name='get_greeting'),
    url(r'^api/conversation/instructions', get_instructions, name='get_instructions'),
    url(r'^api/conversation/answer/positive', get_positive_answer, name='get_positive_answer'),
    url(r'^api/conversation/answer/neutral', get_neutral_answer, name='get_neutral_answer'),
    url(r'^api/conversation/answer/negative', get_negative_answer, name='get_negative_answer'),
    url(r'^api/conversation/salutation', get_salutation, name='get_salutation'),
    url(r'^api/(?P<dataset_id>[\w_@-]+)/correspondances/classes', get_classes_correspondances, name='get_dataset_classes_correspondances'),
    url(r'^api/(?P<dataset_id>[\w_@-]+)/correspondances/properties', get_properties_correspondances, name='get_dataset_classes_correspondances'),
    url(r'^api/(?P<dataset_id>[\w_@-]+)/correspondances', get_correspondances, name='get_dataset_correspondances'),
    url(r'^chatbot/(?P<dataset_id>[\w_@-]+)/?$', semantize, name='chatbot_semantize')
]
