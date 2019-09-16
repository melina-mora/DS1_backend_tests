import requests
from tools.json_tools import extract, dict_to_json


class User:

    def __init__(self, app_config, data, user=None, psswd=None, legal_entity_id=None):
        self._user = extract(body=data, path="$.username") if not user else user
        self._password = extract(body=data, path="$.password") if not psswd else psswd
        self._legal_entity = self.set_legal_entity_id(data=data, legal_entity_id=legal_entity_id)

        self._country = None

        self._env = app_config.env
        self._base_url = app_config.base_url

        self._last_response = None

        self._session = None
        self._session_headers = None

        self.login()

    #LOGIN
    def login(self):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",  # TODO put in config
            "App-Code": "DCMWebTool_App"  # TODO put in config
        }

        body = {
            "grant-type": "password",
            "scope": "security",
            "username": self._user,
            "password": self._password
        }

        url = "/v2/secm/oam/oauth2/token" #TODO put in config

        self._session = self.post(url=url, data=body, headers=headers)
        self.store_session_id(response=self._session)
        self._country = extract(body=self._session.json(), path="$.country")

        return self._session

    #REQUEST
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

    def request(self, url, method, **kwargs):
        url = self._base_url+url

        if 'headers' not in kwargs:
            kwargs['headers'] = self._session_headers

        response = requests.request(url=url, method=method.upper(), **kwargs)

        assert response.status_code in [200, 201]

        self._last_response = response
        return self._last_response

    def get(self, url, **query):
        if query.__len__() > 0:
            url = url + "?"
            for i in query:
                url = url + i + "=" + str(query[i])

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

    # EXPOSE INFORMATION
    def get_legal_entity_id(self):
        return self._legal_entity

    def set_legal_entity_id(self, data, legal_entity_id=None):
        if legal_entity_id is None:
            legal_entity_id = extract(body=data, path="$.legalEntity.legalEntityId")
            if not legal_entity_id:
                raise ValueError("Missing parameter legalEntityId. Check test data or specify.")

        if type(legal_entity_id) is str:
            return legal_entity_id
        else:
            raise ValueError("Should be str with format 'legalEntityId.legalEntityTypeId'. Ex: 1234.1")

    def get_user(self):
        return self._user

    def get_user_country(self):
        return self._country
