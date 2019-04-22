from chatbot import semantic_engine as SemanticEngine

ODS_DATASET_RECORDS = [{
    "record": {
        "id": "a11d01a3b3cf8d24b16fce8749cece22a27efb10",
        "timestamp": "2019-01-01T19:29:40+00:00",
        "size": 749,
        "fields": {
            "reign_start": "0014-09-18T00:00:00+00:00",
            "index": "2",
            "verif_who": "Reddit user zonination",
            "death": "0037-03-16T00:00:00+00:00",
            "name": "Tiberius",
            "name_full": "TIBERIVS CAESAR DIVI AVGVSTI FILIVS AVGVSTVS",
            "killer": "Other Emperor",
            "birth": "0041-11-16T00:00:00+00:00",
            "dynasty": "Julio-Claudian",
            "rise": "Birthright",
            "birth_prv": "Italia",
            "reign_end": "0037-03-16T00:00:00+00:00",
            "era": "Principate",
            "image": {
                "mimetype": "image/jpeg",
                "format": "JPEG",
                "url": "https://data.opendatasoft.com/api/v2/catalog/datasets/roman-emperors@public/files/8a3bf3637985407b3d99e8e9d598f964",
                "color_summary": [
                    "rgba(135, 97, 90, 1.00)",
                    "rgba(131, 98, 89, 1.00)",
                    "rgba(125, 106, 103, 1.00)"
                ],
                "height": 2093,
                "last_synchronized": "2017-12-31T22:00:12.157396",
                "width": 1492,
                "etag": "2a20909ef466b75ddcc6fc641f947d2a",
                "id": "8a3bf3637985407b3d99e8e9d598f964",
                "filename": "Tiberius_NyCarlsberg01.jpg",
                "thumbnail": True
            },
            "cause": "Assassination",
            "notes": "birth is BCE. Assign negative for correct ISO 8601 dates. Possibly assassinated by praetorian guard",
            "birth_cty": "Rome"
        }
    }
}]

ODS_DATASET_FIELDS = {
    "name": "name",
    "label": "Name",
    "type": "text",
    "annotations": {},
    "description": None,
    "class": None
}


class TestSemanticEngine(object):

    def test_field_class_correspondance(self):
        class_correspondance = SemanticEngine.get_field_class(ODS_DATASET_RECORDS, ODS_DATASET_FIELDS, language='en')
        assert class_correspondance
        assert class_correspondance.get('uri')
        assert class_correspondance.get('field_name') == 'name'
        assert class_correspondance.get('label') == 'Name'

    def test_field_property_correspondance(self):
        property_correspondance = SemanticEngine.get_field_property(ODS_DATASET_FIELDS, language='en')
        assert property_correspondance
        assert property_correspondance.get('uri')
        assert property_correspondance.get('field_name') == 'name'
        assert property_correspondance.get('label') == 'Name'
