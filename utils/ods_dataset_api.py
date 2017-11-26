import json

from urllib2 import urlopen, Request, HTTPError
from urllib import urlencode

DATA_RECORD_API_URL = "https://data.opendatasoft.com/api/records/1.0/search/"


class DatasetIdMissing(Exception):
    pass


class UnknownDataset(Exception):
    pass


class ODSDatasetApi(object):
    """This class implements the OpenDataSoft records API v1."""

    @staticmethod
    def dataset_records_request(dataset_id, rows=10):
        """Retrieve dataset's records based on its dataset_id."""
        if dataset_id:
            params = {'dataset': dataset_id, 'rows': rows}
            parameters = "?%s" % urlencode(params)
            return ODSDatasetApi._request("%s%s" % (DATA_RECORD_API_URL, parameters))
        else:
            raise DatasetIdMissing

    @staticmethod
    def _request(url):
        request = Request(url)
        try:
            response = urlopen(request)
        except HTTPError:
            raise UnknownDataset
        raw_data = response.read().decode('utf-8')
        data = json.loads(raw_data)
        return data
