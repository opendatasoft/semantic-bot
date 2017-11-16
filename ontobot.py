import sys

from utils.lov_api import LovApi
from utils.ods_catalog_api import ODSCatalogApi

if len(sys.argv) > 1:
    print ODSCatalogApi.dataset_meta_request(sys.argv[1])
    sys.exit()
else:
    print 'ontobot.py <dataset_id>'
    sys.exit()
