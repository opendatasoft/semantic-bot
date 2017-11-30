import requests

import utils.requester as Requester

ENTITY_EXTRACTION_URL = "https://api.dandelion.eu/datatxt/nex/v1"
# just a free token to test api
TOKEN = '820d18fd5e2a498eb4ebeec9c6c57325'


class QueryParameterMissing(Exception):
    pass


def entity_types_request(query):
    if query:
        params = {'text': query, 'include': 'types', 'token': TOKEN}
        request = requests.get(ENTITY_EXTRACTION_URL, params, timeout=Requester.get_timeout())
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
