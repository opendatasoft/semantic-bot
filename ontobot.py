import sys

from utils.lov_api import LovApi
from utils.ods_catalog_api import ODSCatalogApi
from utils.natural_language_processor import NLProcessor

if len(sys.argv) > 1:
    dataset = ODSCatalogApi.dataset_meta_request(sys.argv[1])
    description = dataset['metas']['description']
    print NLProcessor.extract_noun(description)
    sys.exit()
else:
    print 'ontobot.py <dataset_id>'
    sys.exit()
