from utils import dbpedia_ner as DBpediaNER


class TestDBpediaNER(object):

    def test_NER_DBpedia_FR(self):
        class_list = DBpediaNER.entity_types_request('France', language='fr')
        assert 'Country' in class_list

    def test_NER_DBpedia_EN(self):
        class_list = DBpediaNER.entity_types_request('France', language='en')
        assert 'Country' in class_list

    def test_DBpedia_format(self):
        class_list = DBpediaNER.entity_types_request('New York', language='fr')
        assert 'City' in class_list
