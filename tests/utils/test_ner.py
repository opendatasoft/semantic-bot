from utils import virtuoso_ner as NER


class TestNER(object):

    def test_ner(self):
        class_list = NER.entity_types_request('Tiberius')
        print(class_list)
        assert class_list
