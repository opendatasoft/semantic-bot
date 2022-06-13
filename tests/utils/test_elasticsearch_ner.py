from utils import elasticsearch_ner as ElasticsearchNER


class TestDBpediaNER(object):

    def test_NER_DBpedia(self):
        class_list = ElasticsearchNER.entity_types_request('Opendatasoft')
        assert 'Company' in class_list