from chatbot import semantic_engine as SemanticEngine
from utils import ods_catalog_api as CatalogAPI
from utils import ods_dataset_api as RecordsAPI

ODS_TEST_DATASET_ID = 'arbresremarquablesparis2011@public'


class TestSemanticEngine(object):

    def test_correspondances(self):
        ods_dataset_meta = CatalogAPI.dataset_meta_request(ODS_TEST_DATASET_ID)
        ods_dateset_records = RecordsAPI.dataset_records_request(ODS_TEST_DATASET_ID, rows=5)['records']
        candidate_correspondances = SemanticEngine.init_correspondances_set(ods_dataset_meta, ods_dateset_records)
        assert candidate_correspondances
        assert candidate_correspondances.get('classes')
        assert candidate_correspondances.get('properties')
