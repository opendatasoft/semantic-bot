from utils import virtuoso_ner as NER


class TestDBpediaNER(object):

    def test_ner(self):
        class_list = NER.entity_types_request('Tiberius')
        assert class_list
