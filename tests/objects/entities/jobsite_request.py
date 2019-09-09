from objects.entities.opportunity import Opportunity
from tools.json_tools import extract


class JobsiteRequest(Opportunity):
	def __init__(self, user, code):
		self._user = user
		self._code = code
		self._id = None
		super().__init__(user, code)

	def post_new_jobsite_request(self, legal_entity_id=None, body=None):
		r = self.post_new_opportunity(legal_entity_id=legal_entity_id, body=body)
		self._id = extract(body=r.json(), path="$..opportunityId")
		return r

	def get_jobsite_request_by_ids(self, opportunity=None, opportunity_id=None):
		if opportunity is None and opportunity_id is None:
			raise ValueError("Both opportunity or opportunity_id can't be None.")

		r = self.get_opportunity_by_id(opportunity=opportunity, opportunity_id=opportunity_id)
		return r

	def patch_jobsite_request_address(self, opportunity=None, opportunity_id=None, body=None):
		if opportunity is None and opportunity_id is None:
			raise ValueError("Both opportunity or opportunity_id can't be None.")
		r = self.patch_opportunity_address(opportunity=opportunity, opportunity_id=opportunity_id, body=body)
		return r

	def put_business_lines_in_jobsite_request(self, opportunity=None, opportunity_id=None, body=None):
		if opportunity is None and opportunity_id is None:
			raise ValueError("Both opportunity or opportunity_id can't be None.")
		r = self.put_opportunity_business_lines(opportunity=opportunity, opportunity_id=opportunity_id, body=body)
		return r


