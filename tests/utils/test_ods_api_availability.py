import os
from utils import ods_dataset_api as DatasetAPI
from utils import ods_catalog_api as CatalogAPI

DATASET_ID_TEST = 'arbresremarquablesparis2011@public'

os.environ['DJANGO_SETTINGS_MODULE'] = 'chatbot_app.settings'


class TestODSApiAvailability(object):

    def test_api_catalog_availability(self):
        response = CatalogAPI.dataset_meta_request(DATASET_ID_TEST)
        assert response
        response = CatalogAPI.datasets_meta_request(start=0, rows=5)
        assert response

    def test_apiV2_record_availability(self):
        response = DatasetAPI.dataset_records_request(DATASET_ID_TEST, rows=5)
        assert response
