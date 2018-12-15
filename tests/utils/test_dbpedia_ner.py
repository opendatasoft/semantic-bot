from django.test.testcases import TestCase
from utils import dbpedia_ner as DBpediaNER


class TestDBpediaNER(TestCase):

    def test_DBpedia_FR(self):
        class_list = DBpediaNER.entity_types_request('France', language='fr')
        print class_list
