from tools.json_tools import extract, update_json
from .common.api import Api
from ..api.config import ConfigLogin


class User(Api):

    def __init__(self, app_config, data, user=None, psswd=None, legal_entity_id=None):
        super().__init__(app_config)

        self._user = extract(body=data, path="$.username") if not user else user
        self._password = extract(body=data, path="$.password") if not psswd else psswd

        self._legal_entity = self.set_legal_entity_id(data=data, legal_entity_id=legal_entity_id)

        self._country = None

        self._session = None
        self._session_headers = None

        self.login()

    #LOGIN
    def login(self):
        api = ConfigLogin().configure_test_data_login(env=self._env)
        headers = extract(body=api, path="$..headers")
        body = extract(body=api, path="$..body")

        body = update_json(body=body, values={
            "username": self._user,
            "password": self._password
        })

        url = extract(body=api, path="$..url")

        self._session = self.post(url=url, data=body, headers=headers, login=True)
        self.store_session_id(response=self._session)
        self._country = extract(body=self._session.json(), path="$.country")

        return self._session

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
