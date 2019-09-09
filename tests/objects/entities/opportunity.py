from objects.api.config import ConfigOpportunity
from datetime import datetime
from tools.json_tools import *
from warnings import warn


# Main class for all opportunity type.
class Opportunity:
	def __init__(self, user, code):
		self._code = code
		self._user = user
		self._config = ConfigOpportunity().configure_test_data_opportunities()
		super().__init__()

	def post_new_opportunity(self, legal_entity_id=None, body=None):
		apis = self._config["usp_sm_PostOpportunities_v5"]
		url = extract(body=apis, path="$.url")

		if body is None:
			body = extract(body=apis, path="$.body")
			if legal_entity_id is None:
				legal_entity_id = self._user.get_legal_entity_id()

			update_json(body=body, path='$..legalEntityId', new_value=int(legal_entity_id[0:-2]))
			update_json(body=body, path='$..legalEntityTypeId', new_value=int(legal_entity_id[-1:]))
			update_json(body=body, path='$..shipmentLocationTypeCode', new_value=self._code)

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

	def patch_opportunity_address(self, opportunity=None, opportunity_id=None, body=None):
		apis = self._config["usp_sm_PatchOpportunityById_v5"]

		if opportunity is None and opportunity_id is not None:
			url = extract(body=apis, path="$.url") + str(opportunity_id)
			opportunity = self._user.get(url=url)
		elif opportunity is not None:
			url = extract(body=opportunity.json(), path="$.links.self")
		else:
			raise ValueError("Missing parameters: opportunity or opportunity_id")

		body = self.set_address(opportunity=opportunity, body=body)
		r = self._user.patch(url=url, json=body)
		return r

	def set_address(self, opportunity, body):
		# Fetch user's country:
		user_country = self._user.get_user_country()

		# Set opportunity description:
		opp_title = "aut_test_%s" % datetime.now().strftime("DS1_%Y%m%d_%H%M")

		# Validate region or fetch the first one of the ones available:
		selected_region = extract(body=body, path="$.addressRequest.regionId")
		url = extract(body=opportunity.json(), path="$.addressRequest.links.regions")
		r = self._user.get(url=url)
		region_list = extract(body=r.json(), path="$..regionId", multiple=True)

		if selected_region not in region_list:
			warn(UserWarning("%s not in regions available, set %s instead. Check test data." % (selected_region, region_list[0])))
			selected_region = region_list[0]

		# Now update the whole payload:
		body = update_json(body=body, path="$.addressRequest.regionId", new_value=selected_region)
		body = update_json(body=body, path="$.opportunityDesc", new_value=opp_title)
		body = update_json(body=body, path="$.addressRequest.countryCode", new_value=user_country)

		return body

	def put_opportunity_business_lines(self, opportunity=None, opportunity_id=None, bl_codes=None, bl_ids=None, body=None):

		#Fetch availability of business lines per opportunity
		if opportunity is None and opportunity_id is not None:
			opportunity = self.get_opportunity_by_id(opportunity_id=opportunity_id)
		elif opportunity is None and opportunity_id is None:
			raise ValueError("Missing parameters: opportunity or opportunity_id")

		if body and not bl_codes:
			bl_ids = extract(body=body, path="$..businessLine.businessLineId", multiple=True)
		elif not body and not bl_codes:
			raise ValueError("Missing parameters: body or business line code")

		body = self.set_business_lines(opportunity=opportunity, req_bl_codes=bl_codes, req_bl_ids=bl_ids)

	def fetch_business_lines_config(self, opportunity,):
		url = extract(body=opportunity.json(), path="$.links.configuration")
		config = self._user.get(url=url)

		bls = extract(body=config.json(), path="$.businessLines")

		return bls

	def set_business_lines(self, opportunity, req_bl_codes=None, req_bl_ids=None):

		if req_bl_ids is not None:
			bls_config, bls = self.validate_business_lines_config(opportunity=opportunity, ids=req_bl_ids)
			key = "businessLineId"
		elif req_bl_codes is not None:
			bls_config, bls = self.validate_business_lines_config(opportunity=opportunity, codes=req_bl_codes)
			key = "businessLineCode"
		else:
			raise ValueError("Missing mandatory parameters: req_bl_codes, req_bl_ids")

		body = self.calculate_opp_bl_body(config=bls_config, key=key, values=bls)
		body = json.dumps({"opportunityBusinessLines": body})
		return body


	def calculate_opp_bl_body(self, config, key, values):
		apis = self._config["usp_sm_PatchOpportunityBusinessLineById_v5"]

		body = []
		for value in values:
			for i in range(0, len(config)):
				if value == config[i][key] and self._code == "O":
					body_bl = extract(body=apis, path="$.body_quote.opportunityBusinessLines.businessLine")
					body_bl = update_json(body=body_bl, path="..businessLineId", new_value=value)
					body_bl = update_json(body=body_bl, path="..volume.estimated.comment", new_value="Automated test comment")
					body_bl = update_json(body=body_bl, path="..volume.estimated.quantity.amount", new_value=100)
					body_bl = update_json(body=body_bl, path="..volume.estimated.quantity.unitOfMeasure.unitId",
									   new_value= extract(body=config, path="$.%s.businesslineConfiguration.defaultUnitOfMeasure.unitId" % config[i]))
					body.append(body_bl)
				elif value == config[i][key]:
					body_bl = extract(body=apis, path="$.body.opportunityBusinessLines")
					body_bl = update_json(body=body_bl, path="$..businessLineId", new_value=value)
					body.append(body_bl)

		body = ','.join(map(str, body))
		body = body.replace("\'", "\"")
		return body





	def validate_business_lines_config(self, opportunity, codes=None, ids=None):
		bls_config = self.fetch_business_lines_config(opportunity=opportunity)

		bls = []
		if codes:
			config = extract(body=bls_config, path="$..businessLineCode", multiple=True)
			if config is None:
				assert False, "There are no business lines available for this opportunity."
			for value in codes:
				if value not in config:
					warn(UserWarning("%s not in opportunity configuration. Check test data." % value))
				else:
					bls.append(value)
			if len(bls) == 0:
				warn(UserWarning("Empty values for opportunity, using values from configuration. Check test data." % (config)))
				bls = config
		elif ids:
			config = extract(body=bls_config, path="$..businessLineId", multiple=True)
			if config is None:
				assert False, "There are no business lines available for this opportunity."
			for value in ids:
				if value not in config:
					warn(UserWarning("%s not in opportunity configuration. Check test data." % value))
				else:
					bls.append(value)
			if len(bls) == 0:
				warn(UserWarning("Empty values for opportunity, using values from configuration. Check test data." % (config)))
				bls = config

			return bls_config, bls


	def patch_opportunity_status_requested(self):
		pass

	def patch_opportunity_contact_request(self):
		pass

	def patch_opportunity_document(self):
		pass




