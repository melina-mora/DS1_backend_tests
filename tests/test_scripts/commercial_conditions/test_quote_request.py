from pytest import mark
from objects.entities.user import User
from objects.entities.quote_request import QuoteRequest
from tools.json_tools import extract


@mark.quote_request
@mark.parametrize("code", ["O"])
class QuoteRequestsTests:

    def test_get_quote_request_details(self, app_config, code, load_test_data):
        data = load_test_data()
        u = User(app_config, data=data)

        quote_request = QuoteRequest(u, code=code)
        r = quote_request.post_new()
        r = quote_request.get_opportunity_by_id(opportunity=r)
        return r

    @mark.end2end
    @mark.smoke
    @mark.health_check
    def test_quote_request_end_to_end(self, app_config, code, load_test_data, project_document_data):
        data = load_test_data
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

        print(r.json())
