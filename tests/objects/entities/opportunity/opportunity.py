from objects.api.config import ConfigOpportunity
from tools.json_tools import *


# Main class for all opportunity type.
class Opportunity:

	def __init__(self, user, code):
		self._code = code
		self._user = user
		self._config = ConfigOpportunity().configure_test_data_opportunities()

	def set_opp_config(self):
		return self._config

	def post_new_opportunity(self, legal_entity_id=None, body=None):
		apis = self._config["usp_sm_PostOpportunities_v5"]
		url = extract(body=apis, path="$.url")

		if body is None:
			body = extract(body=apis, path="$.body")
			if legal_entity_id is None:
				legal_entity_id = self._user.get_legal_entity_id()

			body = update_json(body=body, values={
				'$..legalEntityId': int(legal_entity_id[0:-2]),
				'$..legalEntityTypeId': int(legal_entity_id[-1:]),
				'$..shipmentLocationTypeCode': self._code
			})

		r = self._user.post(url=url, json=body)
		return r

	def get_opportunity_by_id(self, opportunity_id=None, opportunity=None):
		if opportunity:
			body = opportunity.json()
			url = extract(body=body, path="$.links.self")
			r = self._user.get(url=url)
		else:
			if len(opportunity_id) > 1:
				r = self.get_opportunity_by_ids(opportunity_id)
			else:
				apis = self._config["usp_sm_GetOpportunitiesById_v5"]
				url = extract(body=apis, path="$.url")
				url = url + opportunity_id
				r = self._user.get(url=url)

		return r

	def get_opportunity_by_ids(self, url=None, opportunity_ids=None):
		if url is None:
			apis = self._config["usp_sm_GetOpportunities_v5"]
			url = extract(body=apis, path="$.url")
			ids = ",".join(opportunity_ids)
			url = url + "?opportunityId=" + ids
		else:
			url = url

		r = self._user.get(url=url)
		return r

	def patch_opportunity_status_requested(self):
		pass

	def patch_opportunity_document(self):
		pass






