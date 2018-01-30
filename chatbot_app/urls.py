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

from chat.views import semantize, get_correspondances, get_classes_correspondances, get_properties_correspondances

urlpatterns = [
    url(r'^api/(?P<dataset_id>[\w_@-]+)/correspondances/classes', get_classes_correspondances, name='get_dataset_classes_correspondances'),
    url(r'^api/(?P<dataset_id>[\w_@-]+)/correspondances/properties', get_properties_correspondances, name='get_dataset_classes_correspondances'),
    url(r'^api/(?P<dataset_id>[\w_@-]+)/correspondances', get_correspondances, name='get_dataset_correspondances'),
    url(r'^chatbot/(?P<dataset_id>[\w_@-]+)/?$', semantize, name='chatbot_semantize')
]
