from utils import virtuoso_ner as NER


class TestNER(object):

    def test_ner(self):
        try:
            class_list = NER.entity_types_request('Tiberius')
        except Exception:
            self.fail("NER returned an exception.")

    def test_ner_char(self):
        try:
            class_list = NER.entity_types_request('t\'es')
        except Exception:
            self.fail("NER returned an exception.")
