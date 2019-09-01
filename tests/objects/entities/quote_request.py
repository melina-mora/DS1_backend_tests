from objects.api.config import ConfigOpportunity
from datetime import datetime


class QuoteRequest:
	def __init__(self, user, code):
		self._config = ConfigOpportunity()

		self._code = code if code == 'O' else None
		self._id = None
		self._content = None

		self._user = user
		self._apis = self._config.configure_test_data_opportunities()

	def post_new(self, legal_entity_id=None, body=None):
		apis = self._apis["usp_sm_PostOpportunities_v5"]
		url = apis["url"]

		if body is None:
			body = apis["body"]
			if legal_entity_id is None:
				legal_entity_id = self._user.get_legal_entity_id()

			body["legalEntity"]["legalEntityId"] = legal_entity_id[0:-2]
			body["legalEntity"]["legalEntityType"]["legalEntityTypeId"] = legal_entity_id[-1:]
			body["shipmentLocationType"]["shipmentLocationTypeCode"] = self._code

		r = self._user.post(url=url, json=body)
		return r

	def patch_address(self, opportunity=None, opportunity_id=None, body=None):
		apis = self._apis["usp_sm_PatchOpportunityById_v5"]

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
