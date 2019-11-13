from pytest import mark

from objects.entities.quote_request import QuoteRequest
from objects.entities.user import User


@mark.quote_request
class QuoteRequestsTests:

    @mark.crm
    @mark.parametrize("country", ["MX"])
    def test_quote_request_with_crm_integration(self, app_config, country, load_test_user, load_document_data):
        user_data = load_test_user(user_type='crm', country=country)
        u = User(app_config, data=user_data)

        quote_request = QuoteRequest(u)

        r = quote_request.post_new()
        r = quote_request.patch_opportunity_address(opportunity=r)
        if country == 'US':
            r = quote_request.patch_taxable_document(opportunity=r, file=load_document_data())
        r = quote_request.patch_project_document(opportunity=r, file=load_document_data())
        r = quote_request.put_opportunity_business_lines(opportunity=r, bl_codes=['RMX'])
        r = quote_request.put_contact_request(opportunity=r)
        r = quote_request.patch_opportunity_status_requested(opportunity=r)

        code = r.json().get('requestCode')

        print('O Requested code generated: %s' % code)
