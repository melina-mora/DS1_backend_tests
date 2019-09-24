from pytest import mark

from objects.entities.jobsite_request import JobsiteRequest
from objects.entities.user import User
from tools.json_tools import extract, pretty_print


@mark.location_request
@mark.parametrize("code", ["R"])
class LocationRequestsTests:

    @mark.smoke
    @mark.crm
    @mark.parametrize("country", ["MX", "CO", "DO", "US", "EG", "GB"])
    def test_location_request_crm(self, app_config, code, country, load_test_data):
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

        pretty_print(r.json())

    @mark.health_check
    @mark.parametrize("country", ["MX"])  # TODO should be for all the countries
    def test_location_request(self, app_config, code, country, load_test_data):
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

        pretty_print(r.json())
