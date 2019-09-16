from pytest import mark
from objects.entities.user import User
from objects.entities.jobsite_request import JobsiteRequest
from tools.json_tools import extract


@mark.location_request
@mark.parametrize("code", ["R"])
class LocationRequestsTests:

	@mark.smoke
	def test_get_jobsite_request_details(self, app_config, code, load_test_data):
		data = load_test_data
		u = User(app_config, data=data)

		jobsite_request = JobsiteRequest(u, code=code)
		res = jobsite_request.post_new()
		res = jobsite_request.get_opportunity_by_id(opportunity=res)
		return res

	@mark.smoke
	def test_create_location_request(self, app_config, code, load_test_data):
		data = load_test_data
		u = User(app_config, data=data)

		jobsite_request = JobsiteRequest(u, code=code)
		r = jobsite_request.post_new()

	@mark.smoke
	def test_patch_address_in_location_request(self, app_config, code, load_test_data):
		data = load_test_data
		u = User(app_config, data=data)

		jobsite_request = JobsiteRequest(u, code=code)
		r = jobsite_request.post_new()
		r = jobsite_request.patch_request_address(opportunity=r,
												  payload=data)

	@mark.smoke
	@mark.skip(reason='Pending fix link new url: PUT /v5/sm/opportunities/{opportunityId:\\d+}/opportunitybusinesslines')
	def test_put_business_lines_in_location_request(self, app_config, code, load_test_data):
		data = load_test_data
		u = User(app_config, data=data)

		jobsite_request = JobsiteRequest(u, code=code)
		r = jobsite_request.post_new()
		r = jobsite_request.put_business_lines(opportunity=r,
											   payload=data)

	@mark.smoke
	def test_put_contact_request_new_in_location_request(self, app_config, code, load_test_data):
		data = load_test_data
		u = User(app_config, data=data)

		jobsite_request = JobsiteRequest(u, code=code)
		r = jobsite_request.post_new()
		r = jobsite_request.put_contact_request(opportunity=r,
												payload=data)

	@mark.end2end
	@mark.health_check
	def test_jobsite_request_end_to_end(self, app_config, code, load_test_data):
		data = load_test_data
		u = User(app_config, data=data)

		jobsite_request = JobsiteRequest(u, code=code)

		r = jobsite_request.post_new()
		opp_id = extract(body=r.json(), path='$.opportunityId')
		r = jobsite_request.patch_opportunity_address(opportunity=r, payload=data)
		r = jobsite_request.put_business_lines(opportunity=r, payload=data)
		r = jobsite_request.get_opportunity_by_id(opportunity_id=opp_id)
		r = jobsite_request.put_contact_request(opportunity=r, payload=data)
		r = jobsite_request.get_opportunity_by_id(opportunity_id=opp_id)
		r = jobsite_request.patch_opportunity_status_requested(opportunity=r)
		r = jobsite_request.get_opportunity_by_id(opportunity_id=opp_id)

		print(r.json())
