import requests

from django.conf import settings

import utils.requester as Requester

ENTITY_EXTRACTION_URL = "https://api.dandelion.eu/datatxt/nex/v1"
# DANDELION_TOKEN should be in your local_settings.py
DANDELION_TOKEN = settings.DANDELION_TOKEN


class QueryParameterMissing(Exception):
    pass


def entity_types_request(query, lang='en'):
    if query:
        params = {'text': query, 'lang': lang, 'include': 'types', 'token': DANDELION_TOKEN}
        request = requests.get(ENTITY_EXTRACTION_URL, params, timeout=Requester.get_timeout(), headers=Requester.create_ods_headers())
        if request.status_code != requests.codes.bad_request:
            request.raise_for_status
            result = request.json()
            if 'annotations' in result and result['annotations']:
                if 'types' in result['annotations'][0]:
                    for i, classe in enumerate(result['annotations'][0]['types']):
                        result['annotations'][0]['types'][i] = classe.split('/')[-1]
                    return result['annotations'][0]['types']
            return None
    else:
        raise QueryParameterMissing
