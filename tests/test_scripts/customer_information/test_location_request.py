from pytest import mark
from objects.entities.user import User
from objects.entities.jobsite_request import JobsiteRequest


@mark.location_request
@mark.parametrize("code", ["R"])
class LocationRequestsTests:

    @mark.smoke
    @mark.dependency(name="create")
    @mark.skip
    def test_create_location_request(self, app_config, code, load_test_data):
        data = load_test_data
        u = User(app_config,
                 user=data['username'],
                 psswd=data['password'])
        u.login()

        jobsite_request = JobsiteRequest(u, code=code)
        r = jobsite_request.post_new()
        return r

    @mark.dependency(name="patch_address", depends=["create"])
    @mark.skip
    def test_patch_address_in_location_request(self, app_config, code, load_test_data):
        data = load_test_data
        u = User(app_config,
                 user=data['username'],
                 psswd=data['password'])
        u.login()

        jobsite_request = JobsiteRequest(u, code=code)
        r = jobsite_request.post_new()
        r = jobsite_request.patch_address(opportunity=r, body=data["test_data"]["address"])

    #@mark.dependency(name="patch_business_lines", depends=["create"])
    def test_put_business_lines_in_location_request(self, app_config, code, load_test_data):
        data = load_test_data
        u = User(app_config,
                 user=data['username'],
                 psswd=data['password'])
        u.login()

        jobsite_request = JobsiteRequest(u, code=code)
        r = jobsite_request.post_new()
        r = jobsite_request.put_business_lines(opportunity=r, body=data["test_data"]["business_lines"])
