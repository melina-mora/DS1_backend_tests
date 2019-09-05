from pytest import mark
from objects.entities.user import User

@mark.case_request
class CaseRequestTests:

    #@mark.skip(reason='still in development')
    def test_cases_are_listed(self, app_config, load_test_data):
        data = load_test_data
        u = User(app_config, user=data['username'], psswd=data['password'])
        r = u.get(url="/v2/im/currencies", currencyId=1)
        assert r.status_code == 200

    @mark.skip(reason='still in development')
    def test_case_request_are_listed(self, app_config, load_test_data):
        pass