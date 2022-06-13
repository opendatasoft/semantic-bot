import os
from utils import lov_ods_api as LOVODSAPI

os.environ['DJANGO_SETTINGS_MODULE'] = 'chatbot_app.settings'


class TestLOVODSApi(object):

    def test_LOV_ODS_class_query(self):
        result_set = LOVODSAPI.term_request('Administrative-Region', term_type='class', language='en')
        assert result_set
        assert result_set['records'][0]['record']['fields']['uri_suffix'] == 'administrative region'

    def test_LOV_ODS_property(self):
        result_set = LOVODSAPI.term_request('Birth_place', term_type='property', language='en')
        assert result_set
        assert result_set['records'][0]['record']['fields']['uri_suffix'] == 'birth place'
