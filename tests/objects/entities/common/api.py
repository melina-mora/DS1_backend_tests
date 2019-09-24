from copy import deepcopy

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

from tools.json_tools import prepare_params


class Api:
    def __init__(self, app_config):
        self._env = app_config.env
        self._base_url = app_config.base_url

    # REQUEST
    def prepare_headers(self, session_headers=None):
        if session_headers:
            headers = {
                "X-IBM-Client-Id": "dd2ee55f-c93c-4c1b-b852-58c18cc7c277",
                "App-Code": "DCMWebTool_App",
                "Accept-Language": "en-US",
                "Authorization": session_headers['access_token'],
                "jwt": session_headers['jwt'],
                "Content-Type": "application/json"
            }
            self._session_headers = headers
        else:
            headers = self._session_headers

        return headers

    def request(self, url, method, login=False, **kwargs):
        if not login:
            url = self._base_url + url

        if 'headers' not in kwargs:
            kwargs['headers'] = deepcopy(self._session_headers)

        if 'data' in kwargs and type(kwargs['data']) is MultipartEncoder:
            mp_encoder = kwargs['data']
            kwargs['headers']['Content-Type'] = mp_encoder.content_type
            response = requests.request(url=url, method=method.upper(), **kwargs)
            assert response.status_code in [200, 201]
            return response

        response = requests.request(url=url, method=method, **kwargs)
        assert response.status_code in [200, 201]
        return response

    def get(self, url, **query):
        if isinstance(query, dict):
            query = prepare_params(**query)
            url = '?'.join([url, query])

        return self.request(url=url, method='get')

    def post(self, url, payload=None, **kwargs):
        return self.request(url=url, json=payload, method='post', **kwargs)

    def patch(self, url, payload=None, **kwargs):
        return self.request(url=url, json=payload, method='patch', **kwargs)

    def put(self, url, payload=None, **kwargs):
        return self.request(url=url, json=payload, method='put', **kwargs)

    def delete(self, url, payload=None, **kwargs):
        return self.request(url=url, json=payload, method='delete', **kwargs)

    # RESPONSE
    def store_session_id(self, response):
        response = response.json()
        env = self._env

        store = {
            'jwt': response['jwt'],
            'access_token': "Bearer %s" % response['oauth2']['access_token'] if env[0:-3] != '_ds' else response['jwt']
        }

        self.prepare_headers(session_headers=store)
