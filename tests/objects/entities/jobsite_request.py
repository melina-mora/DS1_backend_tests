from objects.api.config import ConfigOpportunity
from objects.entities.businesslines import BusinessLines
from datetime import datetime
from tools.json_tools import Parser


class JobsiteRequest:
	def __init__(self, user, code):
		self._config_opportunity = ConfigOpportunity().configure_test_data_opportunities()
		self._business_lines = BusinessLines(user)

		self._code = code if code == 'R' else None
		self._id = None
		self._content = None

		self._user = user

	def post_new(self, legal_entity_id=None, body=None):
		apis = self._config_opportunity["usp_sm_PostOpportunities_v5"]
		url = apis["url"]

		if body is None:
			body = apis["body"]
			if legal_entity_id is None:
				legal_entity_id = self._user.get_legal_entity_id()

			Parser.update_json(body=body, path='$..legalEntityId', new_value=int(legal_entity_id[0:-2]))
			Parser.update_json(body=body, path='$..legalEntityTypeId', new_value=int(legal_entity_id[-1:]))
			Parser.update_json(body=body, path='$..shipmentLocationTypeCode', new_value=self._code)

		r = self._user.post(url=url, json=body)
		return r

	def patch_address(self, opportunity=None, opportunity_id=None, body=None):
		apis = self._config_opportunity["usp_sm_PatchOpportunityById_v5"]

		if opportunity is None and opportunity_id is not None:
			url = apis["url"] + str(opportunity_id)
		elif opportunity is not None:
			url = opportunity.json()
			url = url["links"]["self"]
		else:
			raise ValueError("Missing parameters: opportunity or opportunity_id")

		if body is None:
			body = apis["body"]

		body["opportunityDesc"] = "aut_test_%s" % datetime.now().strftime("DS1_%Y%m%d_%H%M")

		r = self._user.patch(url=url, json=body)
		return r

	def put_business_lines(self, opportunity=None, opportunity_id=None, body=None, default=True):
		if opportunity is None and opportunity_id is not None:
			self._business_lines.validate_business_lines(opportunity_id=opportunity_id)
		elif opportunity is not None:
			self._business_lines.validate_business_lines(opportunity=opportunity)
			config = self.fetch_business_lines_configuration(opportunity=opportunity)



	def set_business_lines(self,business_lines=None):
		self.fetch_business_lines_configuration()

