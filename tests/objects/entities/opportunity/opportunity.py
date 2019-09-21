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

	def post_new_opportunity(self, legal_entity_id=None, payload=None):
		apis = self._config["usp_sm_PostOpportunities_v5"]
		url = extract(body=apis, path="$.url")

		if payload is None:
			payload = extract(body=apis, path="$.body")

		if legal_entity_id is not None:
			self._user.set_legal_entity_id(legal_entity_id=legal_entity_id)

		legal_entity_id = self._user.get_legal_entity_id()

		payload = update_json(body=payload, values={
			'$..legalEntityId': int(legal_entity_id[0:-2]),
			'$..legalEntityTypeId': int(legal_entity_id[-1:]),
			'$..shipmentLocationTypeCode': "%s" % self._code
		})

		r = self._user.post(url=url, payload=payload)
		return r

	def get_opportunity_by_id(self, opportunity_id=None, opportunity=None):
		if opportunity:
			body = opportunity.json()
			url = extract(body=body, path="$.links.self")
			r = self._user.get(url=url)
		else:
			if isinstance(opportunity_id, list):
				r = self.get_opportunity_by_ids(opportunity_id)
			else:
				apis = self._config["usp_sm_GetOpportunitiesById_v5"]
				url = '%s%s' % (extract(body=apis, path="$.url"), str(opportunity_id))
				r = self._user.get(url=url)

		return r

	def get_opportunity_by_ids(self, url=None, opportunity_ids=None):
		if url is None:
			apis = self._config["usp_sm_GetOpportunities_v5"]
			url = "%s?opportunityId=%s" % (extract(body=apis, path="$.url"), ','.join(opportunity_ids))
		else:
			url = url

		r = self._user.get(url=url)
		return r

	def patch_opportunity_status_requested(self, opportunity=None, opportunity_id=None):
		apis = self._config["usp_sm_PatchOpportunityByIdRequested_v5"]
		if opportunity:
			body = opportunity.json()
			url = extract(body=body, path="$.links.requested")
			r = self._user.patch(url=url)
		elif opportunity_id:
			url = '%s%s' % (extract(body=apis, path="$.links.requested"), str(opportunity_id))
			r = self._user.patch(url=url)
		else:
			raise ValueError("Must specify opportunity or opportunity id to patch to RQST.")

		return r







