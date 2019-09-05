from objects.api.config import ConfigCases


class Case:
    def __init__(self, user):
        self._config_cases = ConfigCases().configure_test_data_cases()

        self._code = None
        self._id = None
        self._content = None

        self._user = user

    def get(self, legal_entity_id=None):
        apis = self._config_cases[""]
        url = apis["url"]

        r = self._user.get(url=url)
        return r

    def post(self):
        '''
        Example of POST for an entity.
        :return:
        '''
        pass
