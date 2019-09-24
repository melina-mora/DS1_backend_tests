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
    @mark.parametrize("country", ["MX", "CO", "DO", "US"])
    def test_quote_request_crm(self, app_config, code, country, load_test_data, project_document_data):
        data = load_test_data(is_crm=True, country=country)
        test_file = project_document_data(data=data)
        u = User(app_config, data=data)

        quote_request = QuoteRequest(u, code=code)

        r = quote_request.post_new()
        opp_id = extract(body=r.json(), path='$.opportunityId')
        r = quote_request.patch_opportunity_address(opportunity=r, payload=data)
        r = quote_request.patch_project_document(opportunity=r, file=test_file)
        r = quote_request.get_opportunity_by_id(opportunity_id=opp_id)
        r = quote_request.put_business_lines(opportunity=r, payload=data)
        r = quote_request.get_opportunity_by_id(opportunity_id=opp_id)
        r = quote_request.put_contact_request(opportunity=r, payload=data)
        r = quote_request.get_opportunity_by_id(opportunity_id=opp_id)
        r = quote_request.patch_opportunity_status_requested(opportunity=r)
        r = quote_request.get_opportunity_by_id(opportunity_id=opp_id)

        pretty_print(r.json())
