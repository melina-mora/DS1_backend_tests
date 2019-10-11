from pytest import mark

from objects.entities.jobsite_request import JobsiteRequest
from objects.entities.user import User
from tools.json_tools import pretty_print


@mark.location_request
class LocationRequestsTests:

    @mark.crm
    @mark.parametrize("country", ["MX", "CO", "DO", "US", "EG", "GB"])
    def test_location_request_with_crm_integration(self, app_config, country, load_test_user, load_document_data):
        user_data = load_test_user(user_type='crm', country=country)
        u = User(app_config, data=user_data)

        location_request = JobsiteRequest(u)

        r = location_request.post_new()
        r = location_request.patch_opportunity_address(opportunity=r)
        if country == 'US':
            r = location_request.patch_taxable_document(opportunity=r, file=load_document_data())
        r = location_request.put_opportunity_business_lines(opportunity=r, bl_codes=['RMX', 'CEM', 'AGG'])
        r = location_request.put_contact_request(opportunity=r)
        r = location_request.patch_opportunity_status_requested(opportunity=r)

        pretty_print(r.json())