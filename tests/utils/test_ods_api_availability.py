import os

from django.conf import settings

from utils.ods_api import dataset as DatasetAPI
from utils.ods_api import catalog as CatalogAPI

DATASET_ID_TEST = 'arbresremarquablesparis2011@public'

os.environ['DJANGO_SETTINGS_MODULE'] = 'chatbot_app.settings'


class TestODSApiAvailability(object):

    def test_api_catalog_availability(self):
        response = CatalogAPI.lookup_v2(domain_id='data', dataset_id=DATASET_ID_TEST, api_key=settings.DATA_API_KEY)
        assert response
        response = CatalogAPI.search_v2(domain_id='data', start=0, rows=5, api_key=settings.DATA_API_KEY)
        assert response

    def test_api_record_availability(self):
        response = DatasetAPI.records_v2(domain_id='data',
                                         dataset_id=DATASET_ID_TEST,
                                         rows=5,
                                         api_key=settings.DATA_API_KEY)
        assert response
