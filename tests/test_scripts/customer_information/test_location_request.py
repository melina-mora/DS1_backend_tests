from pytest import mark

from objects.entities.jobsite_request import JobsiteRequest
from objects.entities.user import User
from tools.json_tools import extract


@mark.location_request
@mark.parametrize("code", ["R"])
class LocationRequestsTests:

    @mark.end2end
    @mark.smoke
    @mark.health_check
    @mark.parametrize("country", ["MX", "CO", "DO", "US", "EG", "GB"])
    def test_location_request_end_to_end(self, app_config, code, country, load_test_data):
        data = load_test_data(is_crm=True, country=country)
        u = User(app_config, data=data)

        jobsite_request = JobsiteRequest(u, code=code)

        r = jobsite_request.post_new()
        opp_id = extract(body=r.json(), path='$.opportunityId')
        r = jobsite_request.patch_opportunity_address(opportunity=r, payload=data)
        r = jobsite_request.get_opportunity_by_id(opportunity_id=opp_id)
        r = jobsite_request.put_business_lines(opportunity=r, payload=data)
        r = jobsite_request.get_opportunity_by_id(opportunity_id=opp_id)
        r = jobsite_request.put_contact_request(opportunity=r, payload=data)
        r = jobsite_request.get_opportunity_by_id(opportunity_id=opp_id)
        r = jobsite_request.patch_opportunity_status_requested(opportunity=r)
        r = jobsite_request.get_opportunity_by_id(opportunity_id=opp_id)

        print(r.json())
