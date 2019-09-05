from objects.api.config import ConfigOpportunity
from objects.entities.businesslines import BusinessLines
from datetime import datetime
from tools.json_tools import *


class JobsiteRequest:
	def __init__(self, user, code):
		self._config_opportunity = ConfigOpportunity().configure_test_data_opportunities()
		self._business_lines = BusinessLines(user)

		self._code = code if code == 'R' else None
		self._id = None
		self._content = None

		self._user = user

	def post_new(self, legal_entity_id=None, body=None):
		'''
		Post a new jobsite request, without address, business lines, contact, or document data.
		:param legal_entity_id: Define this to target a specific legalEntityId(customer)
		:param body: Define this to specify a personalized payload for the POST
		:return: Response object
		'''
		apis = self._config_opportunity["usp_sm_PostOpportunities_v5"]
		url = fetch_value_from_json(body=apis, path="$.url")

		if body is None:
			body = fetch_value_from_json(body=apis, path="$.body")
			if legal_entity_id is None:
				legal_entity_id = self._user.get_legal_entity_id()

			update_json(body=body, path='$..legalEntityId', new_value=int(legal_entity_id[0:-2]))
			update_json(body=body, path='$..legalEntityTypeId', new_value=int(legal_entity_id[-1:]))
			update_json(body=body, path='$..shipmentLocationTypeCode', new_value=self._code)

		r = self._user.post(url=url, json=body)
		return r

	def patch_address(self, opportunity=None, opportunity_id=None, body=None): #TODO complete it
		'''
		Patch address information in a jobsite request.
		:param opportunity: Type: Response, mandatory, but optional if opportunity_id specified.
		:param opportunity_id: int, mandatory, but optional if opportunity is specified.
		:param body: Define this to specify a personalized payload for the POST
		:return: Response object
		'''
		apis = self._config_opportunity["usp_sm_PatchOpportunityById_v5"]

		if opportunity is None and opportunity_id is not None:
			url = fetch_value_from_json(body=apis, path="$.url") + str(opportunity_id)
		elif opportunity is not None:
			url = fetch_value_from_json(body=opportunity.json(), path="$.links.self")
		else:
			raise ValueError("Missing parameters: opportunity or opportunity_id")

		if body is None:
			body = fetch_value_from_json(body=apis, path="$.body")

		opp_desc_str = "aut_test_%s" % datetime.now().strftime("DS1_%Y%m%d_%H%M")
		update_json(body=body,path="$.opportunityDesc", new_value=opp_desc_str)

		r = self._user.patch(url=url, json=body)
		return r

	def put_business_lines(self, opportunity=None, opportunity_id=None, body=None, default=True): #TODO complete it
		if opportunity is None and opportunity_id is not None:
			self._business_lines.validate_business_lines(opportunity_id=opportunity_id)
		elif opportunity is not None:
			self._business_lines.validate_business_lines(opportunity=opportunity)
			config = self.fetch_business_lines_configuration(opportunity=opportunity)

	def set_business_lines(self, business_lines=None):
		self.fetch_business_lines_configuration() #TODO complete it

	def patch_taxable_document(self, body=None): #TODO in progress, taxable
		pass

	def patch_contact_request(self, opportunity=None, opportunity_id=None, legal_entity_id=None, body=None):
		pass #TODO in progress, contact request

	def patch_jobsite_requested(self, opportunity=None, opportunity_id=None): #TODO in progress
		pass

