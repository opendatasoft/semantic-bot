import pprint

from utils.ods_api.catalog import search_v2
from utils.ods_api.dataset import records_v2, export_records_v2

PrettyPrinter = pprint.PrettyPrinter(indent=4)


class CatalogIterator:
    def __init__(self, domain_id, where='', search='', refine='', exclude='', rows=10, start=0,
                 sort='explore.popularity_score', api_key=None):
        self.domain_id = domain_id
        self.where = where
        self.search = search
        self.refine = refine
        self.exclude = exclude
        self.rows = rows
        self.start = start
        self.sort = sort
        self.api_key = api_key
        self.cpt = 0
        self.result = search_v2(domain_id, where, search, refine, exclude, rows, start, sort, api_key)
        self.nb_query = 1

    def __len__(self):
        return self.result['total_count']

    def __iter__(self):
        return self

    def __next__(self):
        if self.cpt <= len(self):
            if len(self.result['datasets']) > 0:
                self.cpt += 1
                return CatalogDataset(self.domain_id, self.result['datasets'].pop(0))
            else:
                self.result = search_v2(self.domain_id, self.where, self.search, self.refine, self.exclude, self.rows,
                                        self.start + (self.nb_query * self.rows), self.sort, self.api_key)
                self.nb_query += 1
                if len(self.result['datasets']) > 0:
                    return self.__next__()
        raise StopIteration()


class ExportDatasetIterator:
    def __init__(self, domain_id, dataset_id, where='', search='',  rows=-1, start=0, sort='',
                 select='', api_key=None):
        self.domain_id = domain_id
        self.dataset_id = dataset_id
        self.where = where
        self.search = search
        self.rows = rows
        self.start = start
        self.sort = sort
        self.select = select
        self.api_key = api_key
        self.result = export_records_v2(domain_id, dataset_id, where, search, rows, start, sort, select, 'jsonl',
                                        api_key)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            fields = next(self.result)
            return DatasetRecord(self.domain_id, self.dataset_id, {'record': {'fields': fields}})
        except StopIteration:
            raise StopIteration()


class DatasetIterator:
    def __init__(self, domain_id, dataset_id, where='', search='', refine='', exclude='',  rows=10, start=0, sort='',
                 select='', api_key=None):
        self.domain_id = domain_id
        self.dataset_id = dataset_id
        self.where = where
        self.search = search
        self.refine = refine
        self.exclude = exclude
        self.rows = rows
        self.start = start
        self.sort = sort
        self.select = select
        self.api_key = api_key
        self.cpt = 0
        self.result = records_v2(domain_id, dataset_id, where, search, refine, exclude, rows, start, sort, select,
                                 api_key)
        self.nb_query = 1

    def __len__(self):
        return self.result['total_count']

    def __iter__(self):
        return self

    def __next__(self):
        if self.cpt <= len(self):
            if len(self.result['records']) > 0:
                self.cpt += 1
                return DatasetRecord(self.domain_id, self.dataset_id, self.result['records'].pop(0))
            else:
                self.result = records_v2(self.domain_id, self.dataset_id, self.where, self.search, self.refine,
                                         self.exclude, self.rows, self.start + (self.nb_query * self.rows),
                                         self.sort, self.select, self.api_key)
                self.nb_query += 1
                if len(self.result['records']) > 0:
                    return self.__next__()
        raise StopIteration()


class CatalogDataset:
    def __init__(self, domain_id, json):
        self.domain_id = domain_id
        self.json = json

    def __repr__(self):
        return repr(self.json)

    def __str__(self):
        return str(self.json)

    @property
    def dataset_id(self):
        return self.json.get('dataset', {}).get('dataset_id')

    @property
    def dataset_uid(self):
        return self.json.get('dataset', {}).get('dataset_uid')

    @property
    def has_records(self):
        return self.json.get('dataset', {}).get('has_records')

    @property
    def fields(self):
        return self.json.get('dataset', {}).get('fields')

    @property
    def source_domain_address(self):
        return self.json.get('dataset', {}).get('metas', {}).get('default', {}).get('source_domain_address')

    @property
    def records_count(self):
        return self.json.get('dataset', {}).get('metas', {}).get('default', {}).get('records_count')

    @property
    def title(self):
        return self.json.get('dataset', {}).get('metas', {}).get('default', {}).get('title')

    @property
    def themes(self):
        return self.json.get('dataset', {}).get('metas', {}).get('default', {}).get('theme')

    @property
    def keywords(self):
        return self.json.get('dataset', {}).get('metas', {}).get('default', {}).get('keyword')

    @property
    def publisher(self):
        return self.json.get('dataset', {}).get('metas', {}).get('default', {}).get('publisher')

    @property
    def language(self):
        return self.json.get('dataset', {}).get('metas', {}).get('default', {}).get('language')

    @property
    def license(self):
        return self.json.get('dataset', {}).get('metas', {}).get('default', {}).get('license')

    @property
    def license_url(self):
        license_url = self.json.get('dataset', {}).get('metas', {}).get('default', {}).get('license_url')
        if not license_url:
            license_url = None
        return license_url

    @property
    def rml_mapping(self):
        return self.json.get('dataset', {}).get('metas', {}).get('semantic', {}).get('rml_mapping')

    @property
    def classes(self):
        return self.json.get('dataset', {}).get('metas', {}).get('semantic', {}).get('classes')

    @property
    def properties(self):
        return self.json.get('dataset', {}).get('metas', {}).get('semantic', {}).get('properties')

    @property
    def features(self):
        return self.json.get('dataset', {}).get('features')

    @property
    def links(self):
        return self.json.get('links')


class DatasetRecord:
    def __init__(self, domain_id, dataset_id, json):
        self.domain_id = domain_id
        self.dataset_id = dataset_id
        self.json = json

    def __repr__(self):
        return repr(self.json)

    def __str__(self):
        return str(self.json)

    def __len__(self):
        return self.json.get('record', {}).get('size')

    @property
    def id(self):
        return self.json.get('record', {}).get('id')

    @property
    def timestamp(self):
        return self.json.get('record', {}).get('timestamp')

    @property
    def fields(self):
        return self.json.get('record', {}).get('fields')

    def value(self, field_name):
        return self.json.get('record', {}).get('fields', {}).get(field_name, None)

    @property
    def links(self):
        return self.json.get('links')
