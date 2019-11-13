from objects.api.config import ConfigOpportunity, ConfigCatalog
from scripts.mongo_tools_script.mongo_connection import MongoDBConnection
from tools.json_tools import *


# Main class for all opportunity type.
class Opportunity:

	def __init__(self, user, code):
		self._code = code
		self._user = user
		self._config = ConfigOpportunity().configure_test_data_opportunities()
		self._catalogs = ConfigCatalog().configure_test_data_catalogs()

	def set_opp_config(self):
		return self._config

	def set_opp_catalogs(self):
		return self._catalogs

	def post_new_opportunity(self, legal_entity_id=None, body=None):
		payload = self.fetch_db(coll='JsonModels')
		payload = payload.coll.find_one({'json_model':'new_opportunity'}, {'payload':1,'url':1, '_id':0})
		url = payload.get("url")

		if body is None:
			payload = payload.get("payload")
		else:
			payload = body

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
				url = '%s%s' % (apis.get("url"), str(opportunity_id))
				r = self._user.get(url=url)

		return r

	def get_opportunity_by_ids(self, url=None, opportunity_ids=None):
		if url is None:
			apis = self._config["usp_sm_GetOpportunities_v5"]
			url = "%s?opportunityId=%s" % (apis.get("url"), ','.join(opportunity_ids))
		else:
			url = url

		r = self._user.get(url=url)
		return r

	def patch_opportunity_status_requested(self, opportunity=None, opportunity_id=None):
		if opportunity:
			opp = opportunity.json()
		elif opportunity_id:
			opp = self.get_opportunity_by_id(opportunity_id=opportunity_id).json()
		else:
			raise ValueError("Must specify opportunity or opportunity id to patch to RQST.")

		url = extract(body=opp, path="$.links.requested")
		r = self._user.patch(url=url)
		return r

	def fetch_db(self, db='TestData', coll=None):
		conn = MongoDBConnection(db=db, coll=coll)
		return conn







