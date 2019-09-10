from pytest import mark
from objects.entities.user import User
from objects.entities.jobsite_request import JobsiteRequest
from tools.json_tools import extract, update_json


@mark.location_request
@mark.parametrize("code", ["R"])
class LocationRequestsTests:

    @mark.smoke
    def test_get_jobsite_request_details(self, app_config, code, load_test_data):
        data = load_test_data
        u = User(app_config,
                 user=extract(body=data, path="$.username"),
                 psswd=extract(body=data, path="$.password"))

        jobsite_request = JobsiteRequest(u, code=code)
        res = jobsite_request.post_new_jobsite_request()
        res = jobsite_request.get_opportunity_by_id(opportunity=res)
        return res

    @mark.smoke
    def test_create_location_request(self, app_config, code, load_test_data):
        data = load_test_data
        u = User(app_config,
                 user=extract(body=data, path="$.username"),
                 psswd=extract(body=data, path="$.password"))

        jobsite_request = JobsiteRequest(u, code=code)
        r = jobsite_request.post_new_jobsite_request()

    @mark.smoke
    def test_patch_address_in_location_request(self, app_config, code, load_test_data):
        data = load_test_data
        u = User(app_config,
                 user=extract(body=data, path="$.username"),
                 psswd=extract(body=data, path="$.password"))

        jobsite_request = JobsiteRequest(u, code=code)
        r = jobsite_request.post_new_jobsite_request(legal_entity_id="3991.1")
        r = jobsite_request.patch_jobsite_request_address(opportunity=r,
                                                          body=extract(body=data, path="$.test_data.address"))
        address_request_id_patched = extract(body=r.json(), path="$.addressRequest.addressRequestId")

        assert address_request_id_patched is not None

    @mark.smoke
    @mark.skip(reason='Pending fix link new url: PUT /v5/sm/opportunities/{opportunityId:\d+}/opportunitybusinesslines')
    def test_put_business_lines_in_location_request(self, app_config, code, load_test_data):
        data = load_test_data
        u = User(app_config,
                 user=extract(body=data, path="$.username"),
                 psswd=extract(body=data, path="$.password"))

        jobsite_request = JobsiteRequest(u, code=code)
        r = jobsite_request.post_new_jobsite_request()
        r = jobsite_request.put_business_lines_in_jobsite_request(opportunity=r,
                                                                  body=extract(data, "$.test_data.business_lines"))

    @mark.smoke
    def test_put_contact_request_new_in_location_request(self, app_config, code, load_test_data):
        data = load_test_data
        u = User(app_config,
                 user=extract(body=data, path='$.username'),
                 psswd=extract(body=data, path='$.password'))

        jobsite_request = JobsiteRequest(u, code=code)
        r = jobsite_request.post_new_jobsite_request()
        r = jobsite_request.put_contact_request_in_jobsite_request(opportunity=r,
                                                                   body=extract(data, "$.test_data.contact_request"))
