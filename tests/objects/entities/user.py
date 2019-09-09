import requests
from tools.json_tools import extract


class User:

    def __init__(self, app_config, user, psswd):
        self._user = user
        self._password = psswd
        self._legalEntityId = None
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

        url = "/v2/secm/oam/oauth2/token"

        self._session = self.post(url=url, data=body, headers=headers)
        self.store_session_id(response=self._session)

        value = extract(body=self._session.json(), path="$.customerId")
        self._legalEntityId = "%s.1" % value
        self._country = extract(body=self._session.json(), path="$.country")

        return self._session

    #REQUEST
    def prepare_headers(self, hdrs=None):
        if hdrs:
            headers = {
                "X-IBM-Client-Id": "dd2ee55f-c93c-4c1b-b852-58c18cc7c277",
                "App-Code": "DCMWebTool_App",
                "Accept-Language": "en-US",
                "Authorization": hdrs['access_token'],
                "jwt": hdrs['jwt'],
                "Content-Type": "application/json"
            }
            self._session_headers = headers
        else:
            headers = self._session_headers

        return headers

    def request(self, url, method='get', **kwargs):
        url = self._base_url+url

        if 'headers' not in kwargs:
            kwargs['headers'] = self._session_headers

        method = method.lower()

        response = requests.request(url=url, method=method, **kwargs)

        assert response.status_code in [200, 201]

        self._last_response = response
        return self._last_response

    def get(self, url, **query):
        if query.__len__() > 0 :
            url = url + "?"
            for i in query:
                url = url + i + "=" + str(query[i])

        return self.request(url=url)

    def post(self, url, data=None, **kwargs):
        return self.request(url=url, data=data, method='post', **kwargs)

    def patch(self, url, data=None, **kwargs):
        return self.request(url=url, data=data, method='patch', **kwargs)

    def put(self, url, data=None, **kwargs):
        return self.request(url=url, data=data, method='put', **kwargs)

    def delete(self, url, data=None, **kwargs):
        return self.request(url=url, data=data, method='delete', **kwargs)

    # RESPONSE
    def store_session_id(self, response):
        response = response.json()
        env = self._env

        store = {
            'jwt': response['jwt'],
            'access_token': "Bearer %s" % response['oauth2']['access_token'] if env[0:-3] != '_ds' else response['jwt']
        }

        self.prepare_headers(hdrs=store)

    # EXPOSE INFORMATION
    def get_legal_entity_id(self):
        return self._legalEntityId

    def get_user(self):
        return self._user

    def get_user_country(self):
        return self._country
