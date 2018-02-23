import requests

from django.conf import settings
from hdt import HDTDocument

import os

document = HDTDocument("dbpedia_dump/instance_type.hdt")


def entity_types_request(query, lang='en'):
    print document.nb_subjects
    return ['test']
