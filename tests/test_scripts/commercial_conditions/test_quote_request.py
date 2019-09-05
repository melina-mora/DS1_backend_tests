from pytest import mark
from objects.entities.user import User
from objects.entities.quote_request import QuoteRequest


@mark.quote_request
@mark.parametrize("code", ["O"])
class QuoteRequestsTests:

    @mark.smoke
    @mark.skip(reason="Still in development")
    def test_create_quote_requests(self, app_config, code, load_test_data):
        data = load_test_data
        u = User(app_config,
                 user=data['username'],
                 psswd=data['password'])
        u.login()

        quote_request = QuoteRequest(u, code=code)
        r = quote_request.post_new()
        r = quote_request.patch_address(opportunity=r, body=data["test_data"]["address"])

        assert r.status_code == 200