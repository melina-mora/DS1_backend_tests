from pytest import mark

from objects.entities.quote_request import QuoteRequest
from objects.entities.user import User
from tools.json_tools import extract, pretty_print


@mark.quote_request
@mark.parametrize("code", ["O"])
class QuoteRequestsTests:

    @mark.smoke
    @mark.crm
    @mark.parametrize("country", ["US"])
    def test_quote_request_crm(self, app_config, code, country, load_test_user, load_document_data):
        user_data = load_test_user(user_type='crm', country=country)
        project_file = load_document_data(doc_type='Project')
        u = User(app_config, data=user_data)

        quote_request = QuoteRequest(u, code=code)

        r = quote_request.post_new()
        r = quote_request.patch_opportunity_address(opportunity=r)
        if country == 'US':
            taxable_file = load_document_data(doc_type='Taxable')
            r = quote_request.patch_taxable_document(opportunity=r, file=taxable_file)
        r = quote_request.patch_project_document(opportunity=r, file=project_file)
        r = quote_request.put_business_lines(opportunity=r)
        r = quote_request.put_contact_request(opportunity=r, payload=data)
        r = quote_request.patch_opportunity_status_requested(opportunity=r)

        code = extract(body=r.json(), path='$.requestCode')

        pretty_print(code)
