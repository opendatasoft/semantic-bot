from utils import yago_ner as YagoNER


class TestYagoNER(object):

    def test_NER_Yago(self):
        class_list = YagoNER.entity_types_request('France', language='fr')
        assert 'Countries' in class_list

    def test_Yago_format(self):
        class_list = YagoNER.entity_types_request('New York', language='fr')
        assert 'States of the United States' in class_list
