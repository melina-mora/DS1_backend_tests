from objects.api.config import ConfigOpportunity, ConfigBusinessLines
from datetime import datetime
import json


class JobsiteRequest:
	def __init__(self, user, code):
		self._config_opportunity = ConfigOpportunity().configure_test_data_opportunities()
		self._config_business_lines = ConfigBusinessLines().configure_test_data_business_lines()

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

			body["legalEntity"]["legalEntityId"] = int(legal_entity_id[0:-2])
			body["legalEntity"]["legalEntityType"]["legalEntityTypeId"] = int(legal_entity_id[-1:])
			body["shipmentLocationType"]["shipmentLocationTypeCode"] = self._code

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

	def put_business_lines(self, opportunity=None, opportunity_id=None, body=None):
		config_bl = self._config_business_lines["usp_sm_GetOpportunities_ByOpportunityId_BusinessLines_v6"]
		put_bl = self._config_business_lines["usp_sm_PostOpportunityBusinessLines_v5"]

		# 1. Fetch BL configuration for opportunity
		if opportunity_id:
			available_bls = self._user.get(url=config_bl % opportunity_id)
		elif opportunity:
			url = opportunity.json()
			url = url["links"]["configuration"]
			available_bls = self._user.get(url=url).json()

			for values in available_bls.items():
				if "businessLines" in values:
					bls = []
					for key, value in values:
						if "businessLineId" == key:
							bls.append({
								"businessLine":{
									"businessLineId":value
								}
							})
					return bls

		else:
			raise ValueError("Missing parameters: opportunity or opportunity_id")

		print(available_bls)

		# 2. Compare BL with requested business lines.
		# if not business_lines_codes and not business_lines_ids:
		# 	bls=[]
		# 	for value in available_bls:
		# 		if value == "businessLineId":
