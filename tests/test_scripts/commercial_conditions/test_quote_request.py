from pytest import mark

from objects.entities.quote_request import QuoteRequest
from objects.entities.user import User
from tools.json_tools import extract, pretty_print


@mark.quote_request
@mark.parametrize("code", ["O"])
class QuoteRequestsTests:

    @mark.smoke
    @mark.health_check
    @mark.crm
    @mark.parametrize("country", ["GB"])
    def test_quote_request_crm(self, app_config, code, country, load_test_user, load_project_document_data):
        data = load_test_user(user_type='crm', country=country)
        test_file = load_project_document_data
        u = User(app_config, data=data)

        quote_request = QuoteRequest(u, code=code)

        r = quote_request.post_new()
        r = quote_request.patch_opportunity_address(opportunity=r, payload=data, title='test_rmx_requote_rejected')
        r = quote_request.patch_project_document(opportunity=r, file=test_file)
        r = quote_request.put_business_lines(opportunity=r, bl_codes=['RMX'])
        r = quote_request.put_contact_request(opportunity=r, payload=data)
        r = quote_request.patch_opportunity_status_requested(opportunity=r)

        code = extract(body=r.json(), path='$.requestCode')

        pretty_print(code)
