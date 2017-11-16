import json

from urllib2 import urlopen, Request, HTTPError

DATA_CATALOG_API_URL = "https://data.opendatasoft.com/api/datasets/1.0/%s/"


class ODSNotAvailable(Exception):
    pass


class DatasetIdMissing(Exception):
    pass


class UnknownDataset(Exception):
    pass


class ODSCatalogApi(object):
    """This class implements the OpenDataSoft catalog API."""

    @staticmethod
    def dataset_meta_request(dataset_id):
        """Retrieve dataset's metadatas based on its dataset_id."""
        if dataset_id:
            return ODSCatalogApi._request(DATA_CATALOG_API_URL % dataset_id)
        else:
            raise DatasetIdMissing

    @staticmethod
    def _request(url):
        request = Request(url)
        try:
            response = urlopen(request)
        except HTTPError:
            raise ODSNotAvailable
        raw_data = response.read().decode('utf-8')
        data = json.loads(raw_data)
        if data.get('error'):
            raise UnknownDataset
        return data
